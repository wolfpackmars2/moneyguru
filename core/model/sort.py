# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-01-05
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.gnu.org/licenses/gpl-3.0.html

import re
import unicodedata

# The range of diacritics in Unicode
diacritics = re.compile('[\u0300-\u036f\u1dc0-\u1dff]')

def sort_string(s):
    """Returns a normalized version of 's' to be used for sorting.
    """
    return diacritics.sub('', unicodedata.normalize('NFD', str(s)).lower())
