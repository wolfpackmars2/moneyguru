# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

# This plugin subclasses CurrencyProviderPlugin to provide additional currencies, whose rates are
# provided by Yahoo.

from datetime import date

from core.plugin import CurrencyProviderPlugin

# This is the exception we have to raise when, for some reason, we temporarily can't contact the
# rate provider.
from core.model.currency import RateProviderUnavailable

# We use Python's built-in urlopen to hit Yahoo's server and fetch the rates
from urllib.request import urlopen

# To create a currency provider plugin, one must subclass CurrencyProviderPlugin. You can see more
# details about how to subclass it in plugins.py. It's accessible online at:
# https://github.com/hsoft/moneyguru/blob/master/core/plugin.py
class YahooProviderPlugin(CurrencyProviderPlugin):
    NAME = 'Yahoo currency rates fetcher'
    AUTHOR = "Virgil Dupras"

    # First, we must tell moneyGuru what currencies we support. We have to return a list of tuples
    # containing the code, the name, the decimal precision and a fallback rate for each currencies
    # we want to support.
    def register_currencies(self):
        self.register_currency(
            'ANG', 'Neth. Antilles florin',
            start_date=date(1998, 1, 2), start_rate=0.7961, latest_rate=0.5722)
        self.register_currency(
            'BBD', 'Barbadian dollar',
            start_date=date(2010, 4, 30), start_rate=0.5003, latest_rate=0.5003)
        self.register_currency(
            'BHD', 'Bahraini dinar',
            exponent=3, start_date=date(2008, 11, 8), start_rate=3.1518, latest_rate=2.6603)
        self.register_currency(
            'EGP', 'Egyptian Pound',
            start_date=date(2008, 11, 27), start_rate=0.2232, latest_rate=0.1805)
        self.register_currency(
            'LTL', 'Lithuanian litas',
            start_date=date(2010, 4, 29), start_rate=0.384, latest_rate=0.384)
        self.register_currency(
            'LVL', 'Latvian lats',
            start_date=date(2011, 2, 6), start_rate=1.9136, latest_rate=1.9136)
        self.register_currency(
            'NIO', 'Nicaraguan córdoba',
            start_date=date(2011, 10, 12), start_rate=0.0448, latest_rate=0.0448)
        self.register_currency(
            'SAR', 'Saudi riyal',
            start_date=date(2012, 9, 13), start_rate=0.26, latest_rate=0.26)
        self.register_currency(
            'UAH', 'Ukrainian hryvnia',
            start_date=date(2010, 4, 29), start_rate=0.1266, latest_rate=0.1266)
        return [
            ('XAU', 'Gold (ounce)', 2, 1430.39),
            ('XAG', 'Silver (ounce)', 2, 23.13),
        ]

    # Then, we must implement the rate fetching method. It has to return a float rate that is the
    # value, today of 1 "currency_code" in CAD (Canadian Dollars).
    # This method is called asynchronously, it will not block moneyGuru if it takes a long time to
    # resolve.
    def get_currency_rate_today(self, currency_code):
        # the result of this request is a single CSV line like this:
        # "CADBHD=X",0.3173,"11/7/2008","5:11pm",N/A,N/A,N/A,N/A,N/A
        try:
            url = 'http://download.finance.yahoo.com/d/quotes.csv?s=%sCAD=X&f=sl1d1t1c1ohgv&e=.csv' % currency_code
            with urlopen(url, timeout=10) as response:
                content = response.read().decode('latin-1')
            return float(content.split(',')[1])
        except Exception:
            raise RateProviderUnavailable()

