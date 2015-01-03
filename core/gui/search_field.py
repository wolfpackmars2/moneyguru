# Created By: Virgil Dupras
# Created On: 2008-07-21
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.gnu.org/licenses/gpl-3.0.html

from hscommon.gui.text_field import TextField

class SearchField(TextField):
    def __init__(self, mainwindow):
        TextField.__init__(self)
        self.document = mainwindow.document
    
    def _update(self, newvalue):
        self.document.filter_string = newvalue
    
    def refresh(self):
        self._text = self._value = self.document.filter_string
        self.view.refresh()
  