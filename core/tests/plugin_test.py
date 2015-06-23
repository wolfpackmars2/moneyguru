# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from hscommon.currency import Currency
from hscommon.testutil import eq_
from core.plugin import CurrencyProviderPlugin, ViewPlugin

from .base import TestApp, with_app

@with_app(TestApp)
def test_dont_crash_with_duplicate_currency_register(app):
    # When two currency plugins register the same currency, don't crash, just ignore the second.
    # XXX At the time of this writing, this test is kinda broken because currency registering,
    # which is global, is not re-initialized after each test, so the test passes, but for dubious
    # reasons (the code that makes this test pass, if removed, breaks all tests). I'll refactor
    # currencies shortly to fix this.
    class FooCurrencyProvider(CurrencyProviderPlugin):
        NAME = "Foo currency fetcher"
        def register_currencies(self):
            return [('XXX', "Foo", 2, 1)]

    class BarCurrencyProvider(CurrencyProviderPlugin):
        NAME = "Bar currency fetcher"
        def register_currencies(self):
            return [('XXX', "Bar", 2, 1)]

    app.set_plugins([FooCurrencyProvider, BarCurrencyProvider]) # no crash
    c = Currency('XXX')
    eq_(c.name, "Foo")

@with_app(TestApp)
def test_ignore_duplicate_plugin_names(app):
    # If two plugins have the same name, don't register the second.

    class FooPlugin(ViewPlugin):
        NAME = "Foo"

    class BarPlugin(ViewPlugin):
        NAME = "Foo"

    app.set_plugins([FooPlugin, BarPlugin])
    emptyview = app.new_tab()
    eq_(len(emptyview.plugin_list), 1) # Only one plugin was loaded

