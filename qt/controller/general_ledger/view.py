# Created By: Virgil Dupras
# Created On: 2010-09-12
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from PyQt5.QtWidgets import QVBoxLayout, QAbstractItemView

from ...support.item_view import TableView
from ..base_transaction_view import BaseTransactionView
from .table import GeneralLedgerTable

class GeneralLedgerView(BaseTransactionView):
    def _setup(self):
        self._setupUi()
        self.gltable = GeneralLedgerTable(model=self.model.gltable, view=self.tableView)
        self._setupColumns() # Can only be done after the model has been connected

    def _setupUi(self):
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tableView = TableView(self)
        self.tableView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(False)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setMinimumSectionSize(18)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setDefaultSectionSize(18)
        self.verticalLayout.addWidget(self.tableView)

    def _setupColumns(self):
        h = self.tableView.horizontalHeader()
        h.setSectionsMovable(True) # column drag & drop reorder

    # --- QWidget override
    def setFocus(self):
        self.gltable.view.setFocus()

    # --- Public
    def fitViewsForPrint(self, viewPrinter):
        viewPrinter.fitTable(self.gltable)

