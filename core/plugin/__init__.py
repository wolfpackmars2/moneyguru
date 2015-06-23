# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

# Column is not used in this unit, but is imported to allow plugins to easily be able to import it.
from hscommon.gui.column import Column # noqa

from .api import ( # noqa
    Plugin, ViewPlugin, ReadOnlyTableRow, ReadOnlyTable, ReadOnlyTableView, ReadOnlyTablePlugin,
    CurrencyProviderPlugin, ImportActionPlugin, ImportBindPlugin, EntryMatch
)

def get_all_core_plugin_modules():
    from . import account_list, currency_rates, payee_breakdown, yahoo_currency_provider
    return [account_list, currency_rates, payee_breakdown, yahoo_currency_provider]

