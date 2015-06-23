Plugins
=======

Since moneyGuru v2.5, it's possible to expand moneyGuru's capability through Python plugins. Plugins
are Python 3 source files located in the plugin folder (the location of that folder depends on the
system, but you can open that folder through "File --> Open Plugin Folder"). When moneyGuru
launches, it looks in that folder for plugins to load and for each plugin it finds, it will add an
item to the plugin list located in the "New Tab" view. To open a plugin, simply double-click on the
name of that plugin in the list.

To install a plugin, take the Python file (a ``.py`` file), put it in the plugin folder and
restart moneyGuru.

**Warning.** moneyGuru plugins are not sandboxed, which means that technically, they could contain
malicious code. Only install plugins from trusted sources or after having reviewed the code yourself.

Limitations
-----------

Plugins are still relatively new in moneyGuru's design and they don't allow a hugely broad range
of capabilities. For now, this is the types of plugins that are supported:

* Read-only tables (``ReadOnlyTablePlugin``)
* Currency providers (``CurrencyProviderPlugin``)
* Import Actions (``ImportActionPlugin``)
* Import match bindings (``ImportBindPlugin``)

For read-only tables, the data in the table is not "live" data and thus isn't refreshed when data
in the document changes, so the tab has to be closed and reopened for the data to be refreshed.

But despite those limitations, there's quite a lot of possibilities, especially for custom reports.
Printing, sorting and CSV-copy-pasting (selecting rows, copying data and then pasting it in
Excel/Numbers) work with those tables.

Creating a plugin
-----------------

There's :mod:`a small convenience API <core.plugin>`, but it's a rather slim one. You're mostly
coding straight on top of moneyGuru's code. There's a
:doc:`developer documentation <developer/index>` telling you about moneyGuru's API as a whole.

So, to create a plugin, I'd suggest that you take one of the examples (available
`on Github <https://github.com/hsoft/moneyguru/tree/develop/core/plugin>`__), duplicate it and
try to wade your way through with example comments. 

I'm very interested in knowing about plugin development efforts so don't hesitate to
`contact me <mailto:hsoft@hardcoded.net>`_ if you need help with the development of your plugin.

