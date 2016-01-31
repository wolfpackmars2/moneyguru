# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

# This plugin subclasses CurrencyProviderPlugin to provide additional currencies, whose rates are
# stale, and thus never updated. If you want to add your own fancy weird currency, this is the
# best place.

from datetime import date

from core.plugin import CurrencyProviderPlugin

class StaleProviderPlugin(CurrencyProviderPlugin):
    NAME = 'Stale currencies provider'
    AUTHOR = "Virgil Dupras"

    def register_currencies(self):
        self.register_currency(
            'ATS', 'Austrian schilling',
            start_date=date(1998, 1, 2), start_rate=0.1123, stop_date=date(2001, 12, 31), latest_rate=0.10309)
        self.register_currency(
            'BEF', 'Belgian franc',
            start_date=date(1998, 1, 2), start_rate=0.03832, stop_date=date(2001, 12, 31), latest_rate=0.03516)
        self.register_currency(
            'DEM', 'German deutsche mark',
            start_date=date(1998, 1, 2), start_rate=0.7904, stop_date=date(2001, 12, 31), latest_rate=0.7253)
        self.register_currency(
            'ESP', 'Spanish peseta',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.009334,
            stop_date=date(2001, 12, 31), latest_rate=0.008526)
        self.register_currency(
            'FIM', 'Finnish markka',
            start_date=date(1998, 1, 2), start_rate=0.2611, stop_date=date(2001, 12, 31), latest_rate=0.2386)
        self.register_currency(
            'FRF', 'French franc',
            start_date=date(1998, 1, 2), start_rate=0.2362, stop_date=date(2001, 12, 31), latest_rate=0.2163)
        self.register_currency(
            'GHC', 'Ghanaian cedi (old)',
            start_date=date(1998, 1, 2), start_rate=0.00063, stop_date=date(2007, 6, 29), latest_rate=0.000115)
        self.register_currency(
            'GRD', 'Greek drachma',
            start_date=date(1998, 1, 2), start_rate=0.005, stop_date=date(2001, 12, 31), latest_rate=0.004163)
        self.register_currency(
            'IEP', 'Irish pound',
            start_date=date(1998, 1, 2), start_rate=2.0235, stop_date=date(2001, 12, 31), latest_rate=1.8012)
        self.register_currency(
            'ITL', 'Italian lira',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.000804,
            stop_date=date(2001, 12, 31), latest_rate=0.000733)
        self.register_currency(
            'NLG', 'Netherlands guilder',
            start_date=date(1998, 1, 2), start_rate=0.7013, stop_date=date(2001, 12, 31), latest_rate=0.6437)
        self.register_currency(
            'PTE', 'Portuguese escudo',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.007726,
            stop_date=date(2001, 12, 31), latest_rate=0.007076)
        self.register_currency(
            'SIT', 'Slovenian tolar',
            start_date=date(2002, 3, 1), start_rate=0.006174, stop_date=date(2006, 12, 29), latest_rate=0.006419)
        self.register_currency(
            'TRL', 'Turkish lira',
            exponent=0, start_date=date(1998, 1, 2), start_rate=7.0e-06,
            stop_date=date(2004, 12, 31), latest_rate=8.925e-07)
        self.register_currency(
            'VEB', 'Venezuelan bolivar',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.002827,
            stop_date=date(2007, 12, 31), latest_rate=0.00046)
        self.register_currency(
            'SKK', 'Slovak koruna',
            start_date=date(2002, 3, 1), start_rate=0.03308, stop_date=date(2008, 12, 31), latest_rate=0.05661)

