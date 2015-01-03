# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-12-07
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.gnu.org/licenses/gpl-3.0.html

from PyQt4.QtCore import Qt

MIME_NODEPATHS = 'application/moneyguru.nodepaths'

INDENTATION_OFFSET_ROLE = Qt.UserRole # Returns an offset for the item's indentation

EXTRA_ROLE = Qt.UserRole + 1 # Returns bitwise extra flags defined below
EXTRA_UNDERLINED = 1<<0
EXTRA_UNDERLINED_DOUBLE = 1<<1
EXTRA_SPAN_ALL_COLUMNS = 1<<2
