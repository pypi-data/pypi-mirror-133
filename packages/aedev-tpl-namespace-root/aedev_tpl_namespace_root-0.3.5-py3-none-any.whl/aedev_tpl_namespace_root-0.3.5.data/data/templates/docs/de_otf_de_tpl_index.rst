namespace portions documentation
################################

welcome to the documentation of the portions (app/service modules and sub-packages) of this freely extendable
{namespace_name} namespace (:pep:`420`).


.. include:: features_and_examples.rst


code maintenance guidelines
***************************


portions code requirements
==========================

    * pure python
    * fully typed (:pep:`526`)
    * fully :ref:`documented <{namespace_name}-portions>`
    * 100 % test coverage
    * multi thread save
    * code checks (using pylint and flake8)


design pattern and software principles
======================================

    * `DRY <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_
    * `KISS <http://en.wikipedia.org/wiki/Keep_it_simple_stupid>`_


.. include:: ../CONTRIBUTING.rst


create new namespace
====================

a :pep:`namespace <420>` splits the codebase of a library or framework into multiple project repositories, called
portions (of the namespace). the portions of the `aedev` namespace are providing `the grm tool to create and maintain
any namespace and its portions <https://aedev.readthedocs.io/en/latest/_autosummary/aedev.git_repo_manager.html>`.

the id of a new namespace consists of letters only and has to be available on PYPI. the group-name name gets by default
generated from the namespace name plus the suffix ``'-group'``, so best choose an id that results in a group name that
is available on your repository server.


register a new namespace portion
================================

the registration of a new portion to the {namespace_name} namespace has to be done by one of the namespace maintainers.
a registered portion will automatically be included into this `{namespace_name} namespace documentation`, available at
`ReadTheDocs <https://{namespace_name}.readthedocs.io>`_.

follow the steps underneath to register and add a new portion to the `{namespace_name}` namespace:

1. open a console window and change the current directory to the parent folder of your projects.
2. choose a not-existing/unique name for the new portion (referred as `<portion-name>` in the next steps).
3. run ``grm new-module <portion_name> --namespace={namespace_name}`` to register the portion name within the namespace,
   to create a new project folder `{namespace_name}_<portion-name>` (providing initial project files created from
   templates) and to get a pre-configured git repository (with the remote already set and the initial files committed).
4. run ``cd {namespace_name}_<portion-name>`` to change the current to the new project folder
5. run `pyenv local \<venv_name\> <https://pypi.org/project/pyenv/>`_ to create/prepare a local virtual environment.
6. TDD: add unit tests into the test module `test_{namespace_name}_<portion-name>{PY_EXT}`, prepared within the
   `{TESTS_FOLDER}` sub-folder of your new code project folder.
7. extend the file <portion_name>{PY_EXT} situated in the `{namespace_name}` sub-folder to implement the new portion.
8. run ``grm check-integrity`` to run the linting and unit tests (if they fail go one or two steps back).
9. run ``grm commit`` and ``grm push`` to upload your new portion via to your remote/server repository under the project
   name `{namespace_name}_<portion-name>` in the users group `{repo_group}` (at {repo_root}).


.. _{namespace_name}-portions:

registered namespace package portions
*************************************

the following list contains all registered portions of the {namespace_name} namespace.


.. hint::
    portions with no dependencies are at the begin of the following list. the portions that are depending on other
    portions of the {namespace_name} namespace are listed more to the end.


.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    {portions_import_names}


indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* `portion repositories at {REPO_CODE_DOMAIN} <{repo_root}>`_
* ae namespace `projects <https://gitlab.com/ae-group/projects>` and `documentation <https://ae.readthedocs.io>`
* aedev `projects <https://gitlab.com/aedev-group/projects>` and `documentation <https://aedev.readthedocs.io>`
