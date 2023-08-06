git repository manager user manual
**********************************

installation of grm
===================

to installing this tool open a console window and run the following command::

    pip install aedev_git_repo_manager

after the installation the ``grm`` command will be available in your OS console.


remote server authentication
============================

actions with write access to the remote repository server, like e.g. `push-project`, are requesting authentication via
the :ref:`config-options` `gitToken` and `gitUser`.

.. hint::
   see https://stackoverflow.com/questions/65163081 to disable user/password prompts for fetch and check actions
   that don't need authentication (and not using `gitToken`), like e.g. :func:`~aedev.git_repo_manager._git_fetch`.
   alternatively
   a function _get_repo_url() could be implemented to replace all usages of pdv_str(..., 'repo_url') and 'origin'.


available actions
=================

check the available command line arguments and options by specifying the `--help` command line option::

    grm --help

additional information provided by `grm` on the available/registered actions of a local project are printed to the
console by specifying the `show-actions` action::

    grm show-actions

to get a more verbose output add the `--verbose` and/or :ref:`--debug_level <pre-defined-config-options>` command line
options::

    grm --verbose --debug_level=2 show-actions

an identical abbreviated execution using the short command line options and the shortcut of `show-actions` looks like::

    grm -v -D 2 actions


repository status
=================

several actions are determining the status of a project, like e.g. `show-status`, `show-repo`, `check-integrity` and
`show-versions`.

in order to synchronize the local :data:`~aedev.git_repo_manager.MAIN_BRANCH` branch with any changes done to same
branch on the 'origin' remote, execute `grm` with the `update-project` action.


file patching helper functions
==============================

this portion is also providing some helper functions to patch code and documentation files.

the function :func:`~aedev.git_repo_manager.bump_file_version` increments any part of a version number of a module,
portion, app or package.

templates are patched with the functions :func:`~aedev.git_repo_manager.patch_string` and
:func:`~aedev.git_repo_manager.refresh_templates`.

in conjunction with the template projects of the `aedev` namespace (like e.g. :mod:`aedev.tpl_project`) any common
portions file (even the ``setup.py`` file) can be created/maintained as a template in a single place, and then requested
and updated individually for each portion project.

.. hint::
    via the namespace root project, e.g. `the ae namespace <https://gitlab.com/ae-group/ae>`_ and the
    `this aedev namespace <https://gitlab.com/aedev-group/aedev>`_, their namespace portions are maintainable by `grm`.

