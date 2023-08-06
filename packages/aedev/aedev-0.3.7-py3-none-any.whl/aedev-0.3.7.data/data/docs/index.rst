
..
    THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev_tpl_namespace_root V0.3.6 

namespace portions documentation
################################

welcome to the documentation of the portions (app/service modules and sub-packages) of this freely extendable
aedev namespace (:pep:`420`).


.. include:: features_and_examples.rst


code maintenance guidelines
***************************


portions code requirements
==========================

    * pure python
    * fully typed (:pep:`526`)
    * fully :ref:`documented <aedev-portions>`
    * 100 % test coverage
    * multi thread save
    * code checks (using pylint and flake8)


design pattern and software principles
======================================

    * `DRY - don't repeat yourself <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__
    * `KIS - keep it simple <http://en.wikipedia.org/wiki/Keep_it_simple_stupid>`__


.. include:: ../CONTRIBUTING.rst


create new namespace
====================

a :pep:`namespace <420>` splits the codebase of a library or framework into multiple project repositories, called
portions (of the namespace).

.. hint::
    the portions of the `aedev` namespace are providing `the grm tool to create and maintain
    any namespace and its portions <https://aedev.readthedocs.io/en/latest/_autosummary/aedev.git_repo_manager.html>`__.

the id of a new namespace consists of letters only and has to be available on PYPI. the group-name name gets by default
generated from the namespace name plus the suffix ``'-group'``, so best choose an id that results in a group name that
is available on your repository server.


register a new namespace portion
================================

the registration of a new portion to the aedev namespace has to be done by one of the namespace maintainers.

registered portions will automatically be included into the `aedev namespace documentation`, available at
`ReadTheDocs <https://aedev.readthedocs.io>`__.

follow the steps underneath to register and add a new portion into the `aedev` namespace:

1. open a console window and change the current directory to the parent directory of your projects root folders.
2. choose a not-existing/unique name for the new portion (referred as `<portion-name>` in the next steps).
3. run ``grm --namespace=aedev new-module <portion_name>`` to register the portion name within the namespace,
   to create a new project folder `aedev_<portion-name>` (providing initial project files created from
   templates) and to get a pre-configured git repository (with the remote already set and the initial files unstaged, to
   be extended, staged and finally committed).
4. run ``cd aedev_<portion-name>`` to change the current to the working tree root of the new portion project.
5. run `pyenv local \<venv_name\> <https://pypi.org/project/pyenv/>`__ (or any other similar tool) to create/prepare a
   local virtual environment.
6. fans of TDD are then coding unit tests in the prepared test module `test_aedev_<portion-name>.py`,
   situated within the `tests` sub-folder of your new code project folder.
7. extend the file <portion_name>.py situated in the `aedev` sub-folder to implement the new portion.
8. run ``grm check-integrity`` to run the linting and unit tests (if they fail go one or two steps back).
9. run ``grm prepare``, then amend the commit message within the file `.commit_msg.txt`, then run ``grm commit``
   and ``grm push`` to commit and upload your new portion to your personal remote/server repository fork, and finally
   run ``grm request`` to request the merge/pull into the forked/upstream repository in the users group `aedev-group`
   (at https://gitlab.com/aedev-group).


.. _aedev-portions:

registered namespace package portions
*************************************

the following list contains all registered portions of the aedev namespace.


.. hint::
    portions with no dependencies are at the begin of the following list. the portions that are depending on other
    portions of the aedev namespace are listed more to the end.


.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    aedev.tpl_namespace_root
    aedev.tpl_project
    aedev.git_repo_manager
    aedev.setup_project
    aedev.tpl_app
    aedev.setup_hook


manuals and tutorials
*********************

.. toctree::

    man/git_repo_manager.rst


indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `portion repositories at gitlab.com <https://gitlab.com/aedev-group>`__
* ae namespace `projects <https://gitlab.com/ae-group>`__ and `documentation <https://ae.readthedocs.io>`__
* aedev `projects <https://gitlab.com/aedev-group>`__ and `documentation <https://aedev.readthedocs.io>`__
