# Copyright 2014 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "BSD" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.notify import Listener, Repeater
from hscommon.gui.base import GUIObject
from hscommon.gui.selectable_list import GUISelectableList

from .print_view import PrintView

class DocumentNotificationsMixin:
    """Mixin for listeners of :class:`.Document` notifications."""
    def account_added(self):
        """Account(s) were added to the document."""

    def account_changed(self):
        """Account(s) had some of their properties changed."""

    def account_deleted(self):
        """Account(s) were deleted from the document."""

    def accounts_excluded(self):
        """Account(s) had their exclusion status changed."""

    def budget_changed(self):
        """Budget(s) had some of their properties changed."""

    def budget_deleted(self):
        """Budget(s) were deleted from the document."""

    def custom_date_range_selected(self):
        """We need to open the custom date range dialog."""

    def date_range_changed(self):
        """The current date range was changed."""

    def date_range_will_change(self):
        """The current date range is just about to change."""

    def document_restoring_preferences(self):
        """Our document is restoring its state from preferences."""

    def document_changed(self):
        """The whole doucment has changed (for example, when loading document)."""

    def document_will_close(self):
        """The document is about to be closed."""

    def edition_must_stop(self):
        """If any GUI is currently in editing mode, this has to stop now."""

    def filter_applied(self):
        """A filter has just been applied to our transactions."""

    def first_weekday_changed(self):
        """The First Weekday preferences has been changed."""

    def performed_undo_or_redo(self):
        """An undo or redo operation was just performed."""

    def saved_custom_ranges_changed(self):
        """A custom date range was just saved into one of the slots."""

    def schedule_changed(self):
        """Schedule(s) had some of their properties changed."""

    def schedule_deleted(self):
        """Schedule(s) were deleted from the document."""

    def transaction_changed(self):
        """Transaction(s) had some of their properties changed."""

    def transaction_deleted(self):
        """Transaction(s) were deleted from the document."""

    def transactions_imported(self):
        """Transactions have just been imported into the document."""


class MainWindowNotificationsMixin:
    """Mixin for listeners of :class:`.MainWindow` notifications."""
    def transactions_selected(self):
        """Transactions were just selected."""

    def area_visibility_changed(self):
        """One of the main window's main part had its visibility toggled."""


class SheetViewNotificationsMixin:
    """Mixin for listeners of :class:`.AccountSheetView` notifications."""
    def group_expanded_state_changed(self):
        """A group had its expand status toggled."""


MESSAGES_EVERYTHING_CHANGED = {'document_changed', 'performed_undo_or_redo'}
MESSAGES_DOCUMENT_CHANGED = (
    MESSAGES_EVERYTHING_CHANGED |
    {
        'account_added', 'account_changed', 'account_deleted', 'transaction_changed',
        'transaction_deleted', 'transactions_imported', 'budget_changed', 'budget_deleted',
        'schedule_changed', 'schedule_deleted'
    }
)

class HideableObject:
    """An object receiving notifications, but that is disabled when hidden.

    Notifications can trigger a lot of refreshes all around, and moneyGuru has a lot of GUI elements
    that are hidden most of the time. What we want to achieve here is to delay refreshes triggered
    by notifications until our GUI element is shown again.

    A subclass of this class can define two class-level constants:

    ``INVALIDATING_MESSAGES``: a set of all notifications that invalidate our content.

    ``ALWAYSON_MESSAGES``: A set of all notifications that should be processed even when our element
    is hidden. By default, it contains ``document_restoring_preferences`` because this message isn't
    really about invalidating content, but rather restoring preferences on document load, which is
    very important to do, hidden or not.
    """
    # Messages that invalidates the view if received while it's hidden (its cache will be
    # revalidated upon show)
    INVALIDATING_MESSAGES = set()
    # Messages that are always passed, even if the object is hidden.
    ALWAYSON_MESSAGES = {'document_restoring_preferences'}

    def __init__(self):
        self._hidden = True
        self._invalidated = True

    #--- Protected
    def _process_message(self, msg):
        """*Protected*. Process notification ``msg``.

        Whenever your subclasses receives a notification, call this. It checks whether the
        notification should be processed and invalidates our element if needed.

        Returns ``True`` if our notification should be further processed. ``False`` if not.
        """
        if self._hidden and (msg in self.INVALIDATING_MESSAGES):
            self._invalidated = True
        return (not self._hidden) or (msg in self.ALWAYSON_MESSAGES)

    def _revalidate(self):
        """*Virtual*. Refresh the GUI element's content.

        Override this when you subclass with code that refreshes the content of the element. This is
        called when we show the element back and that we had received a notification invalidating
        our content.
        """

    #--- Public
    def show(self):
        """Show the object and revalidate if necessary.

        If an invalidating notification was received while we were hidden, we'll trigger a full
        refresh with :meth:`_revalidate`.
        """
        self._hidden = False
        if self._invalidated:
            self._revalidate()
            self._invalidated = False

    def hide(self):
        """Hide the object.

        We will no longer process notifications. We'll refresh when we show up again, if needed.
        """
        self._hidden = True


class DocumentGUIObject(Listener, GUIObject, DocumentNotificationsMixin):
    """Base class for listeners of :class:`.Document`.

    This base class is not much more than a convenience layer, centralizing multiple subclassing
    and common properties (:attr:`app` and :attr:`document`). It's a base class for every GUI
    elements that listen to some notifications from :class:`.Document`.

    Subclasses :class:`.Listener`, :class:`.GUIObject` and :class:`DocumentNotificationsMixin`.

    :param document: Reference document.
    :type document: :class:`.Document`
    :param listento: The object to listen our notifications from. Defaults to ``document``.
    :type listento: :class:`.Broadcaster`
    """
    def __init__(self, document, listento=None):
        if listento is None:
            listento = document
        Listener.__init__(self, listento)
        GUIObject.__init__(self)
        #: Parent :class:`document <.Document>`.
        self.document = document
        #: Parent :class:`app <.Application>`.
        self.app = document.app


class MainWindowGUIObject(DocumentGUIObject, MainWindowNotificationsMixin):
    """Base class for listeners of :class:`.MainWindow`.

    This base class is not much more than a convenience layer, centralizing multiple subclassing
    and common properties (:attr:`mainwindow`). It's a base class for every GUI elements that listen
    to some notifications from :class:`.MainWindow`.

    Subclasses :class:`DocumentGUIObject` and :class:`MainWindowNotificationsMixin`.

    :param mainwindow: Reference mainwindow.
    :type mainwindow: :class:`.MainWindow`
    :param listento: The object to listen our notifications from. Defaults to ``mainwindow``.
    :type listento: :class:`.Broadcaster`
    """
    def __init__(self, mainwindow, listento=None):
        if listento is None:
            listento = mainwindow
        DocumentGUIObject.__init__(self, mainwindow.document, listento=listento)
        #: Parent :class:`main window <.MainWindow>`.
        self.mainwindow = mainwindow


class ViewChild(MainWindowGUIObject, HideableObject):
    """Visible GUI element listening to notifications from its parent view.

    Subclasses :class:`.MainWindowGUIObject` and :class:`.HideableObject`.

    :param parent_view: View we listen our notifications from.
    :type parent_view: :class:`BaseView`
    """
    def __init__(self, parent_view):
        MainWindowGUIObject.__init__(self, parent_view.mainwindow, listento=parent_view)
        HideableObject.__init__(self)
        #: Parent :class:`base view <BaseView>`.
        self.parent_view = parent_view

    def _process_message(self, msg):
        # We never want to process messages (such as document_restoring_preferences) when our view
        # is None because it will cause a crash.
        if self.view is None:
            return False
        else:
            return HideableObject._process_message(self, msg)

    def dispatch(self, msg):
        if self._process_message(msg):
            Listener.dispatch(self, msg)


# XXX There's only core.gui.report.Report using this. No need for a base class. Push this back up.
class RestorableChild(ViewChild):
    def __init__(self, parent_view):
        ViewChild.__init__(self, parent_view)
        self._was_restored = False

    def _do_restore_view(self):
        # Virtual. Override this and perform actual restore process. Return True if restoration
        # could be done and False otherwise (for example, if our doc doesn't have a document ID yet
        # or other stuff like that).
        return False

    def restore_view(self):
        if not self._was_restored:
            if self._do_restore_view():
                self._was_restored = True


class GUIPanel(GUIObject):
    """GUI Modal dialog.

    All panels work pretty much the same way: They load up an object's properties, let the user
    fiddle with them, and then save those properties back in the object.

    As :ref:`described in the devdoc overview <writetoamodel>`, saving to an object doesn't mean
    directly doing so. We need to go through the :class:`.Document` to do that. Therefore,
    :meth:`save` doesn't actually do that job, but merely calls the proper document method, with
    the proper arguments.

    Unlike :class:`DocumentGUIObject`, dialogs don't listen to notifications. They're called upon
    explicitly. They do, however, hold references to :attr:`app` and :attr:`document`.

    Subclasses :class:`.GUIObject`.
    """
    def __init__(self, document):
        GUIObject.__init__(self)
        #: Parent :class:`document <.Document>`.
        self.document = document
        #: Parent :class:`app <.Application>`.
        self.app = document.app

    #--- Virtual
    def _load(self):
        """*Virtual*. Load the panel's content.

        The subclass is supposed to know what it has to load from the document (selected
        transaction, selected account, etc.). That's where it does this.
        """
        raise NotImplementedError()

    def _new(self):
        """*Virtual*. Load the panel's content with default values for creation.

        We're creating a new element with our panel. Load it with appropriate initialization values.
        """
        raise NotImplementedError()

    def _save(self):
        """*Virtual*. Save the panel's value into the document.

        Our user confirmed the dialog, thus triggering a save operation. Commit our panel's content
        into our document.
        """
        raise NotImplementedError()

    #--- Overrides
    def load(self, *args, **kwargs):
        """Load the panel's content.

        This :meth:`load operation <_load>` is wrapped in between ``pre_load()`` and ``post_load()``
        calls to the panel's view.

        If you pass arguments to this method, they will be directly passed to :meth:`_load`, thus
        allowing your panel subclasses to take arbitrary arguments.

        If the panel can't load, :exc:`.OperationAborted` will be raised. If a message to the user
        is required, the :exc:`.OperationAborted` exception will have a non-empty message.
        """
        self.view.pre_load()
        self._load(*args, **kwargs)
        self.view.post_load()

    def new(self):
        """Load the panel's content with default values for creation.

        Same as :meth:`load` but with new values.
        """
        self.view.pre_load()
        self._new()
        self.view.post_load()

    def save(self):
        """Save the panel's value into the document.

        This :meth:`save operation <_save>` is preceded by a ``pre_save()`` call to the panel's
        view.
        """
        self.view.pre_save()
        self._save()


class MainWindowPanel(GUIPanel):
    """A :class:`GUIPanel` with :class:`.MainWindow` as a parent.

    The vast, vast majority of panels in moneyGuru.

    Subclasses :class:`GUIPanel`
    """
    def __init__(self, mainwindow):
        GUIPanel.__init__(self, mainwindow.document)
        self.mainwindow = mainwindow


class BaseView(Repeater, GUIObject, HideableObject, DocumentNotificationsMixin, MainWindowNotificationsMixin):
    """Superclass for main "tabs" controllers.

    You know, the tabs you open in moneyGuru (Net Worth, Transactions, General Ledger)? Their main
    controller is a subclass of this. They're a GUI object, but they don't have much of an existence
    as a UI view, their only purpose being to hold the child views together.

    Views subclasses are uniquely identified by their :attr:`VIEW_TYPE` attribute which is an
    ``int`` constant that is kept in sync in the UI layer. This way, when we tell the UI to load up
    the view ``2``, then it knows that we mean the Transactions tab.

    All views respond to a common subset of methods (our virtual methods below), each in their own
    ways. There's many buttons and menu items (new, edit, delete, etc.) that have a name that is
    generic enough to be applied to multiple situations depending on the active tab.
    """
    #--- model -> view calls:
    # restore_subviews_size()
    #

    #: A :class:`.PaneType` constant uniquely identifying our subclass.
    VIEW_TYPE = -1
    #: The class to use as a model when printing a tab. Defaults to :class:`.PrintView`.
    PRINT_VIEW_CLASS = PrintView

    def __init__(self, mainwindow):
        Repeater.__init__(self, mainwindow)
        GUIObject.__init__(self)
        HideableObject.__init__(self)
        self._children = []
        #: :class:`.MainWindow`
        self.mainwindow = mainwindow
        #: :class:`.Document`
        self.document = mainwindow.document
        #: :class:`.Application`
        self.app = mainwindow.document.app
        self._status_line = ""

    #--- Virtual
    def new_item(self):
        """*Virtual*. Create a new item."""
        raise NotImplementedError()

    def edit_item(self):
        """*Virtual*. Edit the selected item(s)."""
        raise NotImplementedError()

    def delete_item(self):
        """*Virtual*. Delete the selected item(s)."""
        raise NotImplementedError()

    def duplicate_item(self):
        """*Virtual*. Duplicate the selected item(s)."""
        raise NotImplementedError()

    def new_group(self):
        """*Virtual*. Create a new group."""
        raise NotImplementedError()

    def navigate_back(self):
        """*Virtual*. Navigate back from wherever the user is coming.

        This may (will) result in the active tab changing.
        """
        raise NotImplementedError()

    def move_up(self):
        """*Virtual*. Move select item(s) up in the list, if possible."""
        raise NotImplementedError()

    def move_down(self):
        """*Virtual*. Move select item(s) down in the list, if possible."""
        raise NotImplementedError()


    #--- Overrides
    def dispatch(self, msg):
        if self._process_message(msg):
            Repeater.dispatch(self, msg)
        else:
            self._repeat_message(msg)

    # This has to be call *once* and *right after creation*. The children are set after
    # initialization so that we can pass a reference to self during children's initialization.
    def set_children(self, children):
        self._children = children
        for child in children:
            child.connect()
        self.restore_subviews_size()

    def show(self):
        HideableObject.show(self)
        for child in self._children:
            child.show()

    def hide(self):
        HideableObject.hide(self)
        for child in self._children:
            child.hide()

    #--- Public
    @classmethod
    def can_perform(cls, action_name):
        """Returns whether our view subclass can perform ``action_name``.

        Base views have a specific set of actions they can perform, and the way they perform these
        actions is defined by the subclasses. However, not all views can perform all actions.
        You can use this method to determine whether a view can perform an action. It does so by
        comparing the method of the view with our base method which we know is abstract and if
        it's not the same, we know that the method was overridden and that we can perform the
        action.
        """
        mymethod = getattr(cls, action_name, None)
        assert mymethod is not None
        return mymethod is not getattr(BaseView, action_name, None)

    def restore_subviews_size(self):
        """*Virtual*. Restore subviews size from preferences."""

    def save_preferences(self):
        """*Virtual*. Save subviews size to preferences."""

    #--- Properties
    @property
    def status_line(self):
        """*get/set*. A short textual description of the global status of the tab.

        This is displayed at the bottom of the main window in the UI.
        """
        return self._status_line

    @status_line.setter
    def status_line(self, value):
        self._status_line = value
        if not self._hidden:
            self.mainwindow.update_status_line()

    #--- Notifications
    def document_restoring_preferences(self):
        self.restore_subviews_size()
        if self.view: # Some BaseView don't have a view
            self.view.restore_subviews_size()


class LinkedSelectableList(GUISelectableList):
    """Selectable list performing an action whenever the selection changes.

    It's a very simple :class:`.GUISelectableList` subclass that takes a ``setfunc`` argument, which
    is a function taking a single ``index`` argument. This function is called whenever our list's
    selection changes, and that newly selected index is passed to our ``setfunc``.
    """
    def __init__(self, items=None, setfunc=None):
        # setfunc(newindex)
        GUISelectableList.__init__(self, items=items)
        self.setfunc = setfunc

    def _update_selection(self):
        GUISelectableList._update_selection(self)
        if self.setfunc is not None:
            self.setfunc(self.selected_index)
