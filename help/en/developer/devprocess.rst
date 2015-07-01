===================
Development Process
===================

moneyGuru is developed using `Test Driven Development`_, leaning heavily toward `iterative
development`_. Refactoring is very frequent, but is done in small steps. The goal is to never have
to make a major rewrite, **but**, at the same time, never be trapped by past design mistakes. We
call that "having your cake and eating it too".

Branches and tags
=================

The git repo has one main branch, ``master``. It represents the latest "stable development commit",
that is, the latest commit that doesn't include in-progress features. This branch should always
be buildable, ``tox`` should always run without errors on it.

When a feature/bugfix has an atomicity of a single commit, it's alright to commit right into
``master``. However, if a feature/bugfix needs more than a commit, it should live in a separate
topic branch until it's ready.

Every release is tagged with the version number. For example, there's a ``2.8.2`` tag for the
v2.8.2 release.

Tests
=====

moneyGuru's development process is different from many other TDD projects because almost all tests
are "high level" (read the `article I wrote about this`_). This means that almost all tests
**exclusively** use publicly available API. By "publicly available API", I don't mean public
methods, I mean that API that is available to the GUI layer. This is why, even though the
``Transaction`` class is a core entity of moneyGuru, it is never tested directly. It (technically,
it's not ``Transaction`` we're testing, it's the behavior that it provides) is always tested through
a GUI element (such as ``core.gui.transaction_table.TransactionTable``).

Although this method empowers the developer with nearly unlimited refactoring potential, it makes
tests harder to write and harder to organize. It is often hard to determine where a test belong and
how it should be written. Tests are divided in two main categories: "gui" tests and "topical" tests.

"gui tests are in ``core.tests.gui`` and cover the behavior of specific gui elements (for example,
"testing if the transaction table has the correct number of rows after adding a new transaction).

The second type of tests live directly in ``core.tests`` and test specific behaviors of the
application (for example, whether split balancing is done correctly). These tests are grouped in
topical units, such as ``split_test``. Note that although these tests don't directly test gui
elements behavior, *they still go through these gui elements to perform their testing*.

Test code is the type of code that is the most dangerous to refactor. moneyGuru has a lot of legacy
test code lying around, in wrong places or in an old coding style (``main_test``, moneyGuru's first
test unit, has a lot of those, which are at the same time core behavioral tests). Although it would
be a good thing to refactor those, it still has to be done very carefully, which rules out a mass
refactoring. Refactoring a test requires the developer to correctly understand the intent of the
test and setup code, which is sometimes not so clear (although all tests must have comments
describing their intent, this description sometimes become irrelevant due to refactorings in the
code). Such an understanding can't be achieved in a mass refactoring. Therefore, the motto is: If
you're playing around a test that you notice need refactoring and that you're confident you can do
it safely, do it.

Tickets
=======

moneyGuru's ticket system is at https://github.com/hsoft/moneyguru/issues . All known bugs and
feature requests are listed there. The way those tickets are organized is described at
https://github.com/hsoft/moneyguru/wiki/issue-labels .

.. _Test Driven Development: http://en.wikipedia.org/wiki/Test-driven_development
.. _iterative development: http://en.wikipedia.org/wiki/Iterative_and_incremental_development
.. _article I wrote about this: http://www.hardcoded.net/articles/high-level-testing
