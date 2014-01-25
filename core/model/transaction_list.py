# Created By: Virgil Dupras
# Created On: 2008-09-14
# Copyright 2014 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from operator import itemgetter

class TransactionList(list):
    """Manages the :class:`.Transaction` instances of a document.
    
    This class is mostly about managing transactions sorting order, moving them around and keeping
    a cache of values to use for completion. There's only one of those in a document, in
    :attr:`.Document.transactions`.
    
    Subclasses ``list``.
    """
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self._descriptions = None
        self._payees = None
        self._account_names = None
    
    #--- Overrides
    def remove(self, transaction):
        """Removes ``transaction`` from the list."""
        list.remove(self, transaction)
        self.clear_cache()
    
    #--- Private
    def _compute_completion_list(self, data_and_mtime):
        """Returns a list of unique data sorted in mtime order.
        
        ``data_and_mtime`` is an iterable containing ``(data, mtime)`` pairs.
        """
        data2mtime = {}
        for data, mtime in data_and_mtime:
            maxmtime = max(mtime, data2mtime.get(data, 0))
            data2mtime[data] = maxmtime
        data_and_mtime = sorted(data2mtime.items(), key=itemgetter(1), reverse=True)
        return [data for data, mtime in data_and_mtime]
    
    def _compute_account_names(self):
        def data_and_mtime_gen():
            for txn in self:
                mtime = txn.mtime
                for account in txn.affected_accounts():
                    yield (account.name, mtime)
        
        self._account_names = self._compute_completion_list(data_and_mtime_gen())
    
    def _compute_descriptions(self):
        data_and_mtime = ((t.description, t.mtime) for t in self)
        self._descriptions = self._compute_completion_list(data_and_mtime)
    
    def _compute_payees(self):
        data_and_mtime = ((t.payee, t.mtime) for t in self)
        self._payees = self._compute_completion_list(data_and_mtime)
    
    #--- Public
    def add(self, transaction, keep_position=False, position=None):
        """Adds ``transaction`` to self
        
        If you want ``transaction.position`` to stay intact, call with ``keep_position`` at True. If
        you  specify a position, this is the one that will be used.
        """
        if position is not None:
            transaction.position = position
        elif not keep_position:
            transactions = self.transactions_at_date(transaction.date)
            if transactions:
                transaction.position = max(t.position for t in transactions) + 1
        self.append(transaction)
        self.clear_cache()
    
    def clear(self):
        """Clears the list of all transactions."""
        del self[:]
        self.clear_cache()
    
    def clear_cache(self):
        """Clears cached data.
        
        For now cache date is auto-completion data (payee, transaction, account). Call this when
        a transaction has been changed.
        """
        self._descriptions = None
        self._payees = None
        self._account_names = None
    
    def reassign_account(self, account, reassign_to=None):
        """Calls :meth:`.Transaction.reassign_account` on all transactions.
        
        If, after such an operation, a transaction ends up referencing no account at all, it is
        removed.
        """
        for transaction in self[:]:
            transaction.reassign_account(account, reassign_to)
            if not transaction.affected_accounts():
                self.remove(transaction)
        self.clear_cache()
    
    def move_before(self, from_transaction, to_transaction):
        """Moves ``from_transaction`` just before ``to_transaction``.
        
        If ``to_transaction`` is ``None``, ``from_transaction`` is moved to the end of the
        list. You must :ref:`recook <cooking>` after having done a move (or a bunch of moves)
        """
        if from_transaction not in self:
            return
        if to_transaction is not None and to_transaction.date != from_transaction.date:
            to_transaction = None
        transactions = self.transactions_at_date(from_transaction.date)
        transactions.remove(from_transaction)
        if not transactions:
            return
        if to_transaction is None:
            target_position = max(t.position for t in transactions) + 1
        else:
            target_position = to_transaction.position
        from_transaction.position = target_position
        for transaction in transactions:
            if transaction.position >= target_position:
                transaction.position += 1
    
    def move_last(self, transaction):
        """Equivalent to :meth:`move_before` with ``to_transaction`` to ``None``."""
        self.move_before(transaction, None)
    
    def transactions_at_date(self, target_date):
        """Returns a set of all transactions occurring on ``target_date``."""
        return set(t for t in self if t.date == target_date)
    
    #--- Properties
    @property
    def account_names(self):
        """A list of account names used in the transactions, in reverse mtime order."""
        if self._account_names is None:
            self._compute_account_names()
        return self._account_names
    
    @property
    def descriptions(self):
        """A list of descriptions used in the transactions, in reverse mtime order."""
        if self._descriptions is None:
            self._compute_descriptions()
        return self._descriptions
    
    @property
    def payees(self):
        """A list of payees used in the transactions, in reverse mtime order."""
        if self._payees is None:
            self._compute_payees()
        return self._payees
    
