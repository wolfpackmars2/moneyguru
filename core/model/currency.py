# Created By: Virgil Dupras
# Created On: 2008-04-22
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from hscommon.currency import Currency, RatesDB

def initialize_db(path):
    """Initialize the app wide currency db if not already initialized."""
    ratesdb = RatesDB(str(path))
    Currency.set_rates_db(ratesdb)

