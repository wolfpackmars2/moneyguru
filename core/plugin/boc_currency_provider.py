# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import re
from datetime import date, datetime
from urllib.parse import urlencode
from urllib.request import urlopen

from core.model.currency import RateProviderUnavailable, USD, EUR, CAD
from core.plugin import CurrencyProviderPlugin

CURRENCY2BOCID = {
    'USD': 'LOOKUPS_IEXE0101',
    'ARS': 'LOOKUPS_IEXE2702',
    'AUD': 'LOOKUPS_IEXE1601',
    'BSD': 'LOOKUPS_IEXE6001',
    'BRL': 'LOOKUPS_IEXE2801',
    'XAF': 'LOOKUPS_IEXE4501',
    'XPF': 'LOOKUPS_IEXE4601',
    'CLP': 'LOOKUPS_IEXE2901',
    'CNY': 'LOOKUPS_IEXE2201',
    'COP': 'LOOKUPS_IEXE3901',
    'HRK': 'LOOKUPS_IEXE6101',
    'CZK': 'LOOKUPS_IEXE2301',
    'DKK': 'LOOKUPS_IEXE0301',
    'XCD': 'LOOKUPS_IEXE4001',
    'EUR': 'LOOKUPS_EUROCAE01',
    'FJD': 'LOOKUPS_IEXE4101',
    'GHS': 'LOOKUPS_IEXE4702',
    'GTQ': 'LOOKUPS_IEXE6501',
    'HNL': 'LOOKUPS_IEXE4301',
    'HKD': 'LOOKUPS_IEXE1401',
    'HUF': 'LOOKUPS_IEXE2501',
    'ISK': 'LOOKUPS_IEXE4401',
    'INR': 'LOOKUPS_IEXE3001',
    'IDR': 'LOOKUPS_IEXE2601',
    'ILS': 'LOOKUPS_IEXE5301',
    'JMD': 'LOOKUPS_IEXE6401',
    'JPY': 'LOOKUPS_IEXE0701',
    'MYR': 'LOOKUPS_IEXE3201',
    'MXN': 'LOOKUPS_IEXE2001',
    'MAD': 'LOOKUPS_IEXE4801',
    'MMK': 'LOOKUPS_IEXE3801',
    'NZD': 'LOOKUPS_IEXE1901',
    'NOK': 'LOOKUPS_IEXE0901',
    'PKR': 'LOOKUPS_IEXE5001',
    'PAB': 'LOOKUPS_IEXE5101',
    'PEN': 'LOOKUPS_IEXE5201',
    'PHP': 'LOOKUPS_IEXE3301',
    'PLN': 'LOOKUPS_IEXE2401',
    'RON': 'LOOKUPS_IEXE6505',
    'RUB': 'LOOKUPS_IEXE2101',
    'RSD': 'LOOKUPS_IEXE6504',
    'SGD': 'LOOKUPS_IEXE3701',
    'SKK': 'LOOKUPS_IEXE6201',
    'ZAR': 'LOOKUPS_IEXE3401',
    'KRW': 'LOOKUPS_IEXE3101',
    'LKR': 'LOOKUPS_IEXE5501',
    'SEK': 'LOOKUPS_IEXE1001',
    'CHF': 'LOOKUPS_IEXE1101',
    'TWD': 'LOOKUPS_IEXE3501',
    'THB': 'LOOKUPS_IEXE3601',
    'TND': 'LOOKUPS_IEXE5701',
    'AED': 'LOOKUPS_IEXE6506',
    'GBP': 'LOOKUPS_IEXE1201',
    'VEF': 'LOOKUPS_IEXE5902',
    'VND': 'LOOKUPS_IEXE6503',
}

class BOCProviderPlugin(CurrencyProviderPlugin):
    NAME = 'Bank of Canada currency rates fetcher'
    AUTHOR = "Virgil Dupras"

    def register_currencies(self):
        self.supported_currency_codes |= {'USD', 'EUR'} # already added
        # In order we want to list them
        USD.priority = 1
        EUR.priority = 2
        self.register_currency(
            'GBP', 'U.K. pound sterling',
            start_date=date(1998, 1, 2), start_rate=2.3397, latest_rate=1.5349, priority=3)
        CAD.priority = 4
        self.register_currency(
            'AUD', 'Australian dollar',
            start_date=date(1998, 1, 2), start_rate=0.9267, latest_rate=0.9336, priority=5)
        self.register_currency(
            'JPY', 'Japanese yen',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.01076, latest_rate=0.01076, priority=6)
        self.register_currency(
            'INR', 'Indian rupee',
            start_date=date(1998, 1, 2), start_rate=0.03627, latest_rate=0.02273, priority=7)
        self.register_currency(
            'NZD', 'New Zealand dollar',
            start_date=date(1998, 1, 2), start_rate=0.8225, latest_rate=0.7257, priority=8)
        self.register_currency(
            'CHF', 'Swiss franc',
            start_date=date(1998, 1, 2), start_rate=0.9717, latest_rate=0.9273, priority=9)
        self.register_currency(
            'ZAR', 'South African rand',
            start_date=date(1998, 1, 2), start_rate=0.292, latest_rate=0.1353, priority=10)
        # The rest, alphabetical
        self.register_currency(
            'AED', 'U.A.E. dirham',
            start_date=date(2007, 9, 4), start_rate=0.2858, latest_rate=0.2757)
        self.register_currency(
            'ARS', 'Argentine peso',
            start_date=date(1998, 1, 2), start_rate=1.4259, latest_rate=0.2589)
        self.register_currency(
            'BRL', 'Brazilian real',
            start_date=date(1998, 1, 2), start_rate=1.2707, latest_rate=0.5741)
        self.register_currency(
            'BSD', 'Bahamian dollar',
            start_date=date(1998, 1, 2), start_rate=1.425, latest_rate=1.0128)
        self.register_currency(
            'CLP', 'Chilean peso',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.003236, latest_rate=0.001923)
        self.register_currency(
            'CNY', 'Chinese renminbi',
            start_date=date(1998, 1, 2), start_rate=0.1721, latest_rate=0.1484)
        self.register_currency(
            'COP', 'Colombian peso',
            start_date=date(1998, 1, 2), start_rate=0.00109, latest_rate=0.000513)
        self.register_currency(
            'CZK', 'Czech Republic koruna',
            start_date=date(1998, 2, 2), start_rate=0.04154, latest_rate=0.05202)
        self.register_currency(
            'DKK', 'Danish krone',
            start_date=date(1998, 1, 2), start_rate=0.2075, latest_rate=0.1785)
        self.register_currency(
            'FJD', 'Fiji dollar',
            start_date=date(1998, 1, 2), start_rate=0.9198, latest_rate=0.5235)
        self.register_currency(
            'GHS', 'Ghanaian cedi',
            start_date=date(2007, 7, 3), start_rate=1.1397, latest_rate=0.7134)
        self.register_currency(
            'GTQ', 'Guatemalan quetzal',
            start_date=date(2004, 12, 21), start_rate=0.15762, latest_rate=0.1264)
        self.register_currency(
            'HKD', 'Hong Kong dollar',
            start_date=date(1998, 1, 2), start_rate=0.1838, latest_rate=0.130385)
        self.register_currency(
            'HNL', 'Honduran lempira',
            start_date=date(1998, 1, 2), start_rate=0.108, latest_rate=0.0536)
        self.register_currency(
            'HRK', 'Croatian kuna',
            start_date=date(2002, 3, 1), start_rate=0.1863, latest_rate=0.1837)
        self.register_currency(
            'HUF', 'Hungarian forint',
            start_date=date(1998, 2, 2), start_rate=0.007003, latest_rate=0.00493)
        self.register_currency(
            'IDR', 'Indonesian rupiah',
            start_date=date(1998, 2, 2), start_rate=0.000145, latest_rate=0.000112)
        self.register_currency(
            'ILS', 'Israeli new shekel',
            start_date=date(1998, 1, 2), start_rate=0.4021, latest_rate=0.2706)
        self.register_currency(
            'ISK', 'Icelandic krona',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.01962, latest_rate=0.00782)
        self.register_currency(
            'JMD', 'Jamaican dollar',
            start_date=date(2001, 6, 25), start_rate=0.03341, latest_rate=0.01145)
        self.register_currency(
            'KRW', 'South Korean won',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.000841, latest_rate=0.000905)
        self.register_currency(
            'LKR', 'Sri Lanka rupee',
            start_date=date(1998, 1, 2), start_rate=0.02304, latest_rate=0.0089)
        self.register_currency(
            'MAD', 'Moroccan dirham',
            start_date=date(1998, 1, 2), start_rate=0.1461, latest_rate=0.1195)
        self.register_currency(
            'MMK', 'Myanmar (Burma) kyat',
            start_date=date(1998, 1, 2), start_rate=0.226, latest_rate=0.1793)
        self.register_currency(
            'MXN', 'Mexican peso',
            start_date=date(1998, 1, 2), start_rate=0.1769, latest_rate=0.08156)
        self.register_currency(
            'MYR', 'Malaysian ringgit',
            start_date=date(1998, 1, 2), start_rate=0.3594, latest_rate=0.3149)
        self.register_currency(
            'NOK', 'Norwegian krone',
            start_date=date(1998, 1, 2), start_rate=0.1934, latest_rate=0.1689)
        self.register_currency(
            'PAB', 'Panamanian balboa',
            start_date=date(1998, 1, 2), start_rate=1.425, latest_rate=1.0128)
        self.register_currency(
            'PEN', 'Peruvian new sol',
            start_date=date(1998, 1, 2), start_rate=0.5234, latest_rate=0.3558)
        self.register_currency(
            'PHP', 'Philippine peso',
            start_date=date(1998, 1, 2), start_rate=0.0345, latest_rate=0.02262)
        self.register_currency(
            'PKR', 'Pakistan rupee',
            start_date=date(1998, 1, 2), start_rate=0.03238, latest_rate=0.01206)
        self.register_currency(
            'PLN', 'Polish zloty',
            start_date=date(1998, 2, 2), start_rate=0.4108, latest_rate=0.3382)
        self.register_currency(
            'RON', 'Romanian new leu',
            start_date=date(2007, 9, 4), start_rate=0.4314, latest_rate=0.3215)
        self.register_currency(
            'RSD', 'Serbian dinar',
            start_date=date(2007, 9, 4), start_rate=0.0179, latest_rate=0.01338)
        self.register_currency(
            'RUB', 'Russian rouble',
            start_date=date(1998, 1, 2), start_rate=0.2375, latest_rate=0.03443)
        self.register_currency(
            'SEK', 'Swedish krona',
            start_date=date(1998, 1, 2), start_rate=0.1787, latest_rate=0.1378)
        self.register_currency(
            'SGD', 'Singapore dollar',
            start_date=date(1998, 1, 2), start_rate=0.84, latest_rate=0.7358)
        self.register_currency(
            'THB', 'Thai baht',
            start_date=date(1998, 1, 2), start_rate=0.0296, latest_rate=0.03134)
        self.register_currency(
            'TND', 'Tunisian dinar',
            exponent=3, start_date=date(1998, 1, 2), start_rate=1.2372, latest_rate=0.7037)
        self.register_currency(
            'TWD', 'Taiwanese new dollar',
            start_date=date(1998, 1, 2), start_rate=0.04338, latest_rate=0.03218)
        self.register_currency(
            'VEF', 'Venezuelan bolivar fuerte',
            start_date=date(2008, 1, 2), start_rate=0.4623, latest_rate=0.2358)
        self.register_currency(
            'VND', 'Vietnamese dong',
            start_date=date(2004, 1, 1), start_rate=8.2e-05, latest_rate=5.3e-05)
        self.register_currency(
            'XAF', 'CFA franc',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.002362, latest_rate=0.002027)
        self.register_currency(
            'XCD', 'East Caribbean dollar',
            start_date=date(1998, 1, 2), start_rate=0.5278, latest_rate=0.3793)
        self.register_currency(
            'XPF', 'CFP franc',
            exponent=0, start_date=date(1998, 1, 2), start_rate=0.01299, latest_rate=0.01114)

    def get_currency_rates(self, currency_code, start_date, end_date):
        form_data = {
            'lookupPage': 'lookup_daily_exchange_rates.php',
            'startRange': '2001-07-07',
            'dFrom': start_date.strftime('%Y-%m-%d'),
            'dTo': end_date.strftime('%Y-%m-%d'),
            'series[]': [
                CURRENCY2BOCID[currency_code],
            ],
        }
        url = 'http://www.bankofcanada.ca/rates/exchange/10-year-lookup/'
        try:
            with urlopen(url, urlencode(form_data, True).encode('ascii')) as response:
                contents = response.read().decode('latin-1')
        except Exception:
            raise RateProviderUnavailable()
        # search for a link to XML data
        match = re.search(r'(?<=")http://www\.bankofcanada\.ca/stats/results//?csv.*?(?=")', contents)
        if not match:
            raise RateProviderUnavailable()
        csv_url = contents[match.start():match.end()]
        with urlopen(csv_url) as csv_file:
            # Our "CSV file" starts with non-CSV data that we don't care about, and at the end,
            # there's the data we care about, starting with a header "Date,currency" (example:
            # "Date,USD"). The rest is a list of lines "date,rate".
            csv_contents = csv_file.read().decode('ascii')
            _, rates_contents = csv_contents.split('\nDate,%s\n' % currency_code)
            lines = rates_contents.splitlines()

            def convert(s):
                sdate, svalue = s.split(',')
                date = datetime.strptime(sdate, '%Y-%m-%d').date()
                try:
                    value = float(svalue)
                except ValueError:
                    # We sometimes have the value "Bank Holiday"
                    value = None
                return (date, value)
            try:
                return [convert(l) for l in lines]
            except Exception:
                raise RateProviderUnavailable()

