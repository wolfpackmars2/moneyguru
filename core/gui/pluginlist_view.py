# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from ..const import PaneType
from .base import BaseView
from .pluginlist_table import PluginListTable

class PluginListView(BaseView):
    VIEW_TYPE = PaneType.PluginList

    def __init__(self, mainwindow):
        BaseView.__init__(self, mainwindow)
        self.table = PluginListTable(document=mainwindow.document)

    def _revalidate(self):
        self.table.refresh()

