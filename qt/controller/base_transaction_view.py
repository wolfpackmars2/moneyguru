# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from core.gui.mass_edition_panel import MassEditionPanel as MassEditionPanelModel
from .base_view import BaseView
from .transaction_panel import TransactionPanel
from .mass_edition_panel import MassEditionPanel

class BaseTransactionView(BaseView):
    # --- model --> view
    def get_panel_view(self, model):
        if isinstance(model, MassEditionPanelModel):
            return MassEditionPanel(model, self.mainwindow)
        else:
            return TransactionPanel(model, self.mainwindow)

