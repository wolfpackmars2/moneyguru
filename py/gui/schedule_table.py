# Created By: Virgil Dupras
# Created On: 2009-08-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from operator import attrgetter

from ..model.amount import convert_amount
from ..model.recurrence import Spawn
from .base import DocumentGUIObject
from .complete import TransactionCompletionMixIn
from .table import GUITable, Row, rowattr
from .transaction_table import TransactionTableRow

class ScheduleTable(DocumentGUIObject, GUITable, TransactionCompletionMixIn):
    def __init__(self, view, document):
        DocumentGUIObject.__init__(self, view, document)
        GUITable.__init__(self)
    
    #--- Override
    def _update_selection(self):
        self.document.select_schedules(self.selected_schedules)
    
    def connect(self):
        DocumentGUIObject.connect(self)
        self.refresh()
        self.view.refresh()
    
    #--- Public
    def refresh(self):
        del self[:]
        for schedule in self.document.scheduled:
            self.append(ScheduleTableRow(self, schedule))
    
    #--- Properties
    @property
    def selected_schedules(self):
        return [row.schedule for row in self.selected_rows]
    
    #--- Event handlers
    def file_loaded(self):
        self.refresh()
        self.view.refresh()
    
    def redone(self):
        self.refresh()
        self.view.refresh()
    
    def undone(self):
        self.refresh()
        self.view.refresh()
    

class ScheduleTableRow(Row):
    def __init__(self, table, schedule):
        Row.__init__(self, table)
        self.document = table.document
        self.schedule = schedule
        self.transaction = schedule.ref
        self.load()
    
    def load(self):
        schedule = self.schedule
        txn = schedule.ref
        self._start_date = txn.date
        self._start_date_fmt = None
        self._stop_date = schedule.stop_date
        self._stop_date_fmt = None
        self._repeat_type = schedule.repeat_type
        self._interval = unicode(schedule.repeat_every)
        self._description = txn.description
        self._payee = txn.payee
        self._checkno = txn.checkno
        splits = txn.splits
        froms, tos = txn.splitted_splits()
        self._from_count = len(froms)
        self._to_count = len(tos)
        UNASSIGNED = 'Unassigned' if len(froms) > 1 else ''
        self._from = ', '.join(s.account.name if s.account is not None else UNASSIGNED for s in froms)
        UNASSIGNED = 'Unassigned' if len(tos) > 1 else ''
        self._to = ', '.join(s.account.name if s.account is not None else UNASSIGNED for s in tos)
        try:
            self._amount = sum(s.amount for s in tos)
        except ValueError: # currency coercing problem
            currency = self.document.app.default_currency
            self._amount = sum(convert_amount(s.amount, currency, transaction.date) for s in tos)
        self._amount_fmt = None
    
    def save(self):
        pass # read-only
    
    # The "get" part of those properies below are called *very* often, hence, the format caching
    
    @property
    def start_date(self):
        if self._start_date_fmt is None:
            self._start_date_fmt = self.table.document.app.format_date(self._start_date)
        return self._start_date_fmt
    
    @property
    def stop_date(self):
        if self._stop_date_fmt is None:
            if self._stop_date is None:
                self._stop_date_fmt = ''
            else:
                self._stop_date_fmt = self.table.document.app.format_date(self._stop_date)
        return self._stop_date_fmt
    
    repeat_type = rowattr('_repeat_type')
    interval = rowattr('_interval')
    description = rowattr('_description')
    payee = rowattr('_payee')
    checkno = rowattr('_checkno')
    from_ = rowattr('_from')
    to = rowattr('_to')

    @property
    def amount(self):
        if self._amount_fmt is None:
            self._amount_fmt = self.document.app.format_amount(self._amount)
        return self._amount_fmt
    