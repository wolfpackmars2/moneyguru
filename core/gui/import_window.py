# Created By: Virgil Dupras
# Created On: 2008-08-07
# Copyright 2014 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "BSD" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.hardcoded.net/licenses/bsd_license

# To avoid clashing with "first" in the "first/second" pattern being all over the place in this
# unit, we rename our imported first() function here
from hscommon.util import flatten, dedupe, first as getfirst
from hscommon.trans import tr
from collections import defaultdict

from hscommon.notify import Listener
from ..exception import OperationAborted
from ..model.date import DateFormat
from .base import MainWindowGUIObject, LinkedSelectableList
from .import_table import ImportTable
from core.plugin import ImportActionPlugin, ImportBindPlugin, EntryMatch
from core.document import ImportDocument
from core.model.account import Account
from core.model.entry import Entry


DAY = 'day'
MONTH = 'month'
YEAR = 'year'

# Could be a good target for hscommon.util?
def unique_groups(lst, keyfunc):
    """Given a list and a keyfunction, return lists of all objects with the same key"""
    results = defaultdict(list)
    for itm in lst:
        results[keyfunc(itm)].append(itm)
    return results.values()

class SwapType:
    DayMonth = 0
    MonthYear = 1
    DayYear = 2
    DescriptionPayee = 3
    InvertAmount = 4


class ActionSelectionOptions:
    ApplyToPane = 0
    ApplyToAll = 1  # Ordering is important to respect legacy code (0/1 : False/True comparisons)
    ApplyToSelection = 2


def last_two_digits(year):
    return year - ((year // 100) * 100)


def swapped_date(date, first, second):
    attrs = {DAY: date.day, MONTH: date.month, YEAR: last_two_digits(date.year)}
    newattrs = {first: attrs[second], second: attrs[first]}
    if YEAR in newattrs:
        newattrs[YEAR] += 2000
    return date.replace(**newattrs)


def swap_format_elements(format, first, second):
    # format is a DateFormat
    swapped = format.copy()
    elems = swapped.elements
    TYPE2CHAR = {DAY: 'd', MONTH: 'M', YEAR: 'y'}
    first_char = TYPE2CHAR[first]
    second_char = TYPE2CHAR[second]
    first_index = [i for i, x in enumerate(elems) if x.startswith(first_char)][0]
    second_index = [i for i, x in enumerate(elems) if x.startswith(second_char)][0]
    elems[first_index], elems[second_index] = elems[second_index], elems[first_index]
    return swapped


class InvertAmountsPlugin(ImportActionPlugin):

    NAME = "Invert Amounts Import Action Plugin"
    ACTION_NAME = "Invert Amount"

    def perform_action(self, import_document, transactions, panes, selected_rows=None):
        for transaction in transactions:
            new = transaction.replicate()
            for split in new.splits:
                split.amount = -split.amount
            import_document.change_transaction(transaction, new)


class BaseSwapFields(ImportActionPlugin):

    def _switch_function(self, transaction):
        pass

    def perform_action(self, import_document, transactions, panes, selected_rows=None):
        for txn in transactions:
            new = txn.replicate()
            self._switch_function(new)
            import_document.change_transaction(txn, new)


class SwapDescriptionPayeeAction(BaseSwapFields):

    ACTION_NAME = tr("Description <--> Payee")
    NAME = "Swap Description Payee Import Action Plugin"

    def _switch_function(self, txn):
        txn.description, txn.payee = txn.payee, txn.description


class BaseSwapDateFields(BaseSwapFields):

    def __init__(self):
        super().__init__()
        self._first_field = None
        self._second_field = None

    def _switch_function(self, transaction):
        transaction.date = swapped_date(transaction.date, self._first_field, self._second_field)

    def on_selected_pane_changed(self, selected_pane):
        self._change_name(selected_pane.parsing_date_format)

    def _change_name(self, parsing_date_format):
        basefmt = parsing_date_format
        swapped = swap_format_elements(basefmt, self._first_field, self._second_field)
        self.ACTION_NAME = "{} --> {}".format(basefmt.iso_format, swapped.iso_format)
        self.notify(self.action_name_changed)

    def can_perform_action(self, import_document, transactions, panes, selected_rows=None):
        try:
            for txn in transactions:
                swapped_date(txn.date, self._first_field, self._second_field)
            return True
        except ValueError:
            return False

    def perform_action(self, import_document, transactions, panes, selected_rows=None):
        BaseSwapFields.perform_action(self, import_document, transactions, panes, selected_rows=None)
        # Now, lets' change the date format on these panes
        for pane in panes:
            basefmt = pane.parsing_date_format
            swapped = swap_format_elements(basefmt, self._first_field, self._second_field)
            pane.parsing_date_format = swapped

        self._change_name(panes[0].parsing_date_format)


class SwapDayMonth(BaseSwapDateFields):

    ACTION_NAME = "<placeholder> Day <--> Month"

    NAME = "Swap Day and Month Import Action Plugin"

    def __init__(self):
        super().__init__()
        self._first_field = DAY
        self._second_field = MONTH


class SwapDayYear(BaseSwapDateFields):

    ACTION_NAME = "<placeholder> Day <--> Year"

    NAME = "Swap Day and Year Import Action Plugin"

    def __init__(self):
        super().__init__()
        self._first_field = DAY
        self._second_field = YEAR


class SwapMonthYear(BaseSwapDateFields):

    ACTION_NAME = "<placeholder> Month <--> Year"

    NAME = "Swap Month and Year Import Action Plugin"

    def __init__(self):
        super().__init__()
        self._first_field = MONTH
        self._second_field = YEAR


class ReferenceBind(ImportBindPlugin):

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries):
        matches = []
        import_reference2entry = {}
        will_import = True
        for import_entry in (e for e in imported_entries if e.reference):
            import_reference2entry[import_entry.reference] = import_entry

        for existing_entry in existing_entries:
            if existing_entry.reference in import_reference2entry:
                import_entry = import_reference2entry[existing_entry.reference]
                if existing_entry.reconciled:
                    will_import = False

                del import_reference2entry[existing_entry.reference]
            else:
                import_entry = None

            if import_entry is not None:
                matches.append((existing_entry, import_entry, will_import, 0.99))
            elif not will_import:
                matches.append((existing_entry, import_entry, will_import, 0.99))


        return matches


class AccountPane:
    def __init__(self, import_document, account, target_account):
        self.import_document = import_document
        self.parsing_date_format = self.import_document.parsing_date_format
        self.reference_plugin = ReferenceBind()
        self.account = account
        self._selected_target = target_account
        self.name = account.name
        self.count = len(account.entries)
        self.matches = [] # [[ref, imported]]
        self.max_day = 31
        self.max_month = 12
        self.max_year = 99 # 2 digits
        self._match_entries = dict()
        self._user_binds = dict()  # tracks binds / unbinds as indicated by the user.
        self._match_probabilties = dict()
        self.to_import = dict()
        self.match_flag = False
        self.match_entries()

    def _remove_match(self, match):
        if match.existing in self._match_entries:
            del self._match_entries[match.existing]
        if match.imported in self._match_entries:
            del self._match_entries[match.imported]

    def _determine_best_matches(self, matches):

        def check_better(key, weight):
            conflict = self._match_entries.get(key, None)
            if conflict and conflict.probability < weight:
                self._remove_match(conflict)

        # Take existing entry that is recommended to be mapped to an import entry
        for existing_entry, imported_entry, will_import, weight in matches:
            import_key = self._get_matching_key(imported_entry)
            check_better(existing_entry, weight)
            check_better(import_key, weight)

            if (existing_entry not in self._match_entries and
                import_key not in self._match_entries):
                new_match = EntryMatch(existing_entry, import_key, will_import, weight)
                self._match_entries[existing_entry] = new_match
                self._match_entries[import_key] = new_match


    def _convert_matches(self):

        import_entries = self.import_entries

        existing_entries = self.existing_entries

        self.matches.clear()
        self.to_import.clear()

        processed = set()

        def append_entry(entry, is_import):

            if (((is_import and self._get_matching_key(entry) in processed) or
                 entry in processed)):
                return

            key = self._get_matching_key(entry) if is_import else entry
            match_entry = self._match_entries.get(key, None)

            if (match_entry and
                  match_entry.existing not in processed and
                  match_entry.imported not in processed):
                if is_import:
                    self.matches.append([match_entry.existing, entry])
                else:
                    [import_entry] = [e for e in import_entries
                                      if self._get_matching_key(e) == match_entry.imported]
                    self.matches.append([entry, import_entry])
                processed.add(match_entry.existing)
                processed.add(match_entry.imported)

                if match_entry.will_import:
                    self.to_import[match_entry.imported] = match_entry.will_import
                elif match_entry.existing.reconciled:
                    self.to_import[match_entry.imported] = False

            elif is_import:
                self.matches.append([None, entry])
            elif not entry.reconciled:
                self.matches.append([entry, None])

            processed.add(key)

        user_binds = self._user_binds.items()
        for (existing_entry, import_entry), bound in user_binds:
            new_import_entry = self._get_matching_entry(import_entry, import_entries)
            if new_import_entry is None:
                del self._user_binds[(existing_entry, import_entry)]
                continue
            if bound:
                self.matches.append([existing_entry, import_entry])
                processed.add(existing_entry)
                processed.add(import_entry)


        for existing_entry in existing_entries:
            append_entry(existing_entry, False)

        for import_entry in import_entries:
            append_entry(import_entry, True)

        for (existing_entry, import_entry), bound in self._user_binds.items():
            if not bound:
                import_entry = self._get_matching_entry(import_entry, import_entries)
                match = [[e, i] for [e, i] in self.matches if
                         e and i and
                         (e, i) == (existing_entry, import_entry)]
                if match:
                    [[e, i]] = match
                    self.matches.remove([e, i])
                else:
                    continue
                #if not e.reconciled?
                self.matches.append([e, None])
                self.matches.append([None, i])

    @staticmethod
    def _get_matching_entry(entry, entry_list):
        for e in entry_list:
            if e == entry:
                return e
        return None

    def match_entries(self, binding_plugins=None, import_entries=None):
        self.account = self.import_document.accounts.find(self.name)
        import_entries = self.account.entries[:] if not import_entries else import_entries
        existing_entries = self.existing_entries

        # Making the way for extension of binding plugins
        binding_plugins = [self.reference_plugin]

        for plugin in binding_plugins:
            matches = plugin.match_entries(self.selected_target,
                                           None,
                                           self.import_document,
                                           existing_entries,
                                           import_entries)

            self._determine_best_matches(matches)

        self._convert_matches()
        self._sort_matches()
        self.match_flag = True

    def _sort_matches(self):
        def key_func(t):
            if None not in t:
                return_date = t[1].date
            elif t[0]:
                return_date =t[0].date
            else:
                return_date = t[1].date
            return return_date, t[0] is None

        self.matches.sort(key=key_func)

    def _get_matching_key(self, entry):
        return entry

    def bind(self, existing, imported):
        self._user_binds[(existing, imported)] = True  # Bind
        self._convert_matches()
        self._sort_matches()

    def unbind(self, existing, imported):
        self._user_binds[(existing, imported)] = False  # Unbind
        self._convert_matches()
        self._sort_matches()

    @property
    def selected_target(self):
        return self._selected_target

    @selected_target.setter
    def selected_target(self, value):
        if self._selected_target is value:
            return
        self._selected_target = value
        self._user_binds.clear()
        self._match_entries.clear()
        self.matches.clear()
        self.match_entries()

    @property
    def import_entries(self):
        return self.import_document.accounts.find(self.name).entries[:]

    @property
    def existing_entries(self):
        if not self.selected_target:
            return []
        else:
            return self.selected_target.entries[:]


class ImportWindow(MainWindowGUIObject):
    #--- View interface
    # close()
    # close_selected_tab()
    # refresh_tabs()
    # refresh_target_accounts()
    # set_swap_button_enabled(enabled: bool)
    # show()
    # update_selected_pane()
    #

    def __init__(self, mainwindow):
        MainWindowGUIObject.__init__(self, mainwindow)
        self._selected_pane_index = 0
        self._selected_target_index = 0
        self._import_action_plugins = [SwapDayMonth(),
                                       SwapMonthYear(),
                                       SwapDayYear(),
                                       SwapDescriptionPayeeAction(),
                                       InvertAmountsPlugin()]
        self._always_import_action_plugins = []

        self._import_action_listeners = []
        self._add_plugin_listeners(self._import_action_plugins)
        print("receiving plugins")
        self._recieve_plugins(self.app.plugins)

        def setfunc(index):
            self.view.set_swap_button_enabled(self.can_perform_swap())
        self.swap_type_list = LinkedSelectableList(items=[
            plugin.ACTION_NAME for plugin in self._import_action_plugins
        ], setfunc=setfunc)
        self.swap_type_list.selected_index = SwapType.DayMonth
        self.panes = []
        self.import_table = ImportTable(self)

    #--- Private

    def _collect_action_params(self, import_action, apply=ActionSelectionOptions.ApplyToPane):
        if apply == ActionSelectionOptions.ApplyToSelection:
            if not self.selected_pane:
                return []

            panes = [self.selected_pane]
            selected_rows = self.import_table.selected_rows

            if not selected_rows:
                return []

            transactions = [row.imported.transaction for row in selected_rows if row.imported]
            transactions = dedupe(transactions)
            can_perform_action = import_action.can_perform_action(panes[0].import_document,
                                                                  transactions,
                                                                  panes,
                                                                  selected_rows)
            if not can_perform_action:
                return []

            return [(panes[0].import_document, transactions, panes, selected_rows)]

        if apply == ActionSelectionOptions.ApplyToAll:
            panes = self.panes.copy()
        else:
            panes = [self.selected_pane]
        results = []

        # Groups of panes which share the same import document
        pane_groups = unique_groups(panes, lambda p: p.import_document)
        selected_group = None
        for ps in pane_groups:
            transactions = [e.transaction for p in ps for e in p.account.entries]
            transactions = dedupe(transactions)
            can_perform_action = import_action.can_perform_action(ps[0].import_document, transactions, ps)
            if not can_perform_action:
                continue
            if self.selected_pane in ps:
                selected_group = (ps[0].import_document, transactions, ps)
            else:
                results.append((ps[0].import_document, transactions, ps))
        # We want to ensure that the selected pane group is the last to be called
        # allowing the name of the plugin to update.
        if selected_group:
            results.append(selected_group)
        return results

    def _perform_action(self, import_action, apply=ActionSelectionOptions.ApplyToPane):
        if self.selected_pane is None:
            return

        action_params = self._collect_action_params(import_action, apply)

        if not action_params:
            return

        panes = dedupe(flatten((grp[2] for grp in action_params)))

        for pane in panes:
            pane.match_flag = False
            pane.import_document.cook_flag = False

        for action_param in action_params:
            import_action.perform_action(*action_param)

        for pane in panes:
            if not pane.import_document.cook_flag:
                pane.import_document.cook()

        for pane in panes:
            if not pane.match_flag:
                pane.match_entries()

        self.import_table.refresh()

    def _always_perform_actions(self):
        for plugin in self._always_import_action_plugins:
            self._perform_action(plugin, True)

    def _refresh_target_selection(self):
        if not self.panes:
            return
        target = self.selected_pane.selected_target
        self._selected_target_index = 0
        if target is not None:
            try:
                self._selected_target_index = self.target_accounts.index(target) + 1
            except ValueError:
                pass
        self.import_table.refresh()

    def _refresh_swap_list_items(self):
        if not self.panes:
            return

        # I think, possibly due to the "XXX should be replaced with _updated_selected...
        # comment that exists refresh panes, we aren't kicking off the seleced pane change
        # in time.  So we'll just tell it that the selected pane changed even if it hasn't.

        for index, plugin in enumerate(self._import_action_plugins):
            self._import_action_listeners[index].disconnect()
            plugin.on_selected_pane_changed(self.selected_pane)
            self._import_action_listeners[index].connect()
        names = [plugin.ACTION_NAME for plugin in self._import_action_plugins]
        self.swap_type_list[:] = names

    def _update_selected_pane(self):
        self.import_table.refresh()
        if self.selected_pane:
            for plugin in self._import_action_plugins:
                plugin.on_selected_pane_changed(self.selected_pane)
        self._refresh_swap_list_items()
        self.view.update_selected_pane()
        self.view.set_swap_button_enabled(self.can_perform_swap())

    def _recieve_plugins(self, plugins):
        extended_plugins = [plugin() for plugin in plugins
                            if issubclass(plugin, ImportActionPlugin)]

        select_actions = [p for p in extended_plugins if not p.always_perform_action()]
        always_actions = [p for p in extended_plugins if p.always_perform_action()]

        self._import_action_plugins.extend(select_actions)
        self._add_plugin_listeners(select_actions)
        self._always_import_action_plugins.extend(always_actions)

    def _add_plugin_listeners(self, plugins):
        listeners = [Listener(plugin) for plugin in plugins
                     if not plugin.always_perform_action()]
        for listener in listeners:
            listener.bind_messages((ImportActionPlugin.action_name_changed,),
                                   lambda: self._refresh_swap_list_items())
            listener.connect()
            self._import_action_listeners.append(listener)

    #--- Override
    def _view_updated(self):
        self.connect()
        if self.document.can_restore_from_prefs():
            # See MainWindow._view_updated() comment.
            self.document_restoring_preferences()

    #--- Public

    def can_perform_swap(self):
        index = self.swap_type_list.selected_index
        import_action = self._import_action_plugins[index]
        action_params = self._collect_action_params(import_action, True)
        # We actually perform can_perform_action as part of the _collect_action_params
        # so we don't need to run the explicit check twice, just check to see if
        # the seleced pane was one of the "passing" panes.
        # Also, we consider having no panes unable to perform all actions (mimicing
        # prior implementation)
        if not action_params:
            return False
        else:
            return True

    def close_pane(self, index):
        was_selected = index == self.selected_pane_index
        del self.panes[index]
        if not self.panes:
            self.view.close()
            return
        self._selected_pane_index = min(self._selected_pane_index, len(self.panes) - 1)
        if was_selected:
            self._update_selected_pane()

    def import_selected_pane(self):
        pane = self.selected_pane
        matches = []
        for ref, e in pane.matches:
            if e is None:
                continue

            if e in pane.to_import and not pane.to_import[e]:
                continue

            matches.append((e, ref))

        name2account = pane.import_document.exported_accounts
        cached_txn = pane.import_document.cached_transactions

        def copy_account(acct):
            if acct is None:
                return None
            if acct.name not in name2account:
                copied_account = Account(acct.name, acct.currency, acct.type)
                copied_account.reference = acct.reference
                name2account[acct.name] = copied_account
                return copied_account
            else:
                return name2account[acct.name]

        def copy_transaction(txn):
            if txn not in cached_txn:
                new_txn = txn.replicate()
                cached_txn[txn] = new_txn
                return new_txn
            else:
                return pane.import_document.cached_transactions[txn]


        try:
            pane_account = copy_account(pane.account)

            new_matches = []

            for (e, ref) in matches:
                for indx, s in enumerate(e.transaction.splits):
                    if e.split.uid == s.uid:
                        split_indx = indx
                        break
                transaction = copy_transaction(e.transaction)
                for split in transaction.splits:
                    split.account = copy_account(split.account)

                split = transaction.splits[split_indx]
                new_entry = Entry(split, e.amount, e.balance, e.reconciled_balance, e.balance_with_budget)
                new_matches.append((new_entry, ref))


            if pane.selected_target is not None:
                # We import in an existing account, adjust all the transactions accordingly
                target_account = pane.selected_target
            else:
                target_account = pane_account # pane.account == new account

            self.document.import_entries(target_account, pane_account, new_matches)

        except OperationAborted:
            pass
        else:
            self.close_pane(self.selected_pane_index)
            self.view.close_selected_tab()

    def perform_swap(self, apply=ActionSelectionOptions.ApplyToPane):
        index = self.swap_type_list.selected_index
        import_action = self._import_action_plugins[index]
        self._perform_action(import_action, apply)

    def refresh_targets(self):
        self.target_accounts = [a for a in self.document.accounts if a.is_balance_sheet_account()]
        self.target_accounts.sort(key=lambda a: a.name.lower())

    def refresh_panes(self):
        for pane in self.panes:
            pane.import_document.cook()

        if not hasattr(self.mainwindow, 'loader'):
            return

        # there are ramifications here to think about in terms of expected behavior.
        # old behavior is to store accounts without importing segregated by their respective
        # loader account lists...
        # self.import_document.clear()

        import_document = ImportDocument(self.app)

        self.refresh_targets()
        accounts = [a for a in self.mainwindow.loader.accounts if a.is_balance_sheet_account() and a.entries]

        parsing_date_format = DateFormat.from_sysformat(self.mainwindow.loader.parsing_date_format)
        import_document.reset_from_loader(self.mainwindow.loader, parsing_date_format)
        import_document.cook()
        for account in accounts:
            target_account = None
            if self.mainwindow.loader.target_account is not None:
                target_account = self.mainwindow.loader.target_account
            elif account.reference:
                target_account = getfirst(
                    t for t in self.target_accounts if t.reference == account.reference
                )
            self.panes.append(AccountPane(import_document,
                                          account,
                                          target_account))
        # XXX Should replace by _update_selected_pane()?

        self._always_perform_actions()
        self._refresh_target_selection()
        self._refresh_swap_list_items()
        self.import_table.refresh()

    def show(self):
        self.refresh_panes()
        self.view.refresh_target_accounts()
        self.view.refresh_tabs()
        self.view.show()

    #--- Properties
    @property
    def selected_pane(self):
        return self.panes[self.selected_pane_index] if self.panes else None

    @property
    def selected_pane_index(self):
        return self._selected_pane_index

    @selected_pane_index.setter
    def selected_pane_index(self, value):
        if value >= len(self.panes):
            return
        self._selected_pane_index = value
        self._refresh_target_selection()
        self._update_selected_pane()

    @property
    def selected_target_account(self):
        return self.selected_pane.selected_target

    @property
    def selected_target_account_index(self):
        return self._selected_target_index

    @selected_target_account_index.setter
    def selected_target_account_index(self, value):
        target = self.target_accounts[value - 1] if value > 0 else None
        self.selected_pane.selected_target = target
        self._selected_target_index = value
        self.import_table.refresh()

    @property
    def target_account_names(self):
        return [tr('< New Account >')] + [a.name for a in self.target_accounts]

    #--- Events
    def account_added(self):
        self.refresh_targets()
        self._refresh_target_selection()
        self.view.refresh_target_accounts()

    account_changed = account_added
    account_deleted = account_added

    def document_will_close(self):
        self.import_table.columns.save_columns()

    def document_restoring_preferences(self):
        self.import_table.columns.restore_columns()
