"""
This module can be used for example in running deploy pipelines or githooks
(some code automatically executed before commit). This module can run the tests,
edit library version, generate rst files for docs, push to git or deploy app to pypi.

All of that can be done with one function call - with `push_pipeline` function that
run other functions, or you can use functions separately. 


Examples:
=========

    **VS Code Task example**

    You can push changes with single click with all the hooks displaying results in
    your terminal. All params changing every push (like git message or tag) can
    be configured on the beginning and therefore you don't need to wait for test finish.
    Default values can be also used, so in small starting projects, push is actually very fast.

    Create folder utils, create `push_script.py` inside, add::

        import mypythontools

        if __name__ == "__main__":
            # Params that are always the same define here. Params that are changing define in IDE when run action.
            # For example in tasks (command line arguments and argparse will be used).
            mypythontools.utils.push_pipeline(deploy=True)

    Then just add this task to global tasks.json::

        {
          "version": "2.0.0",
          "tasks": [
            {
              "label": "Build app",
              "type": "shell",
              "command": "python",
              "args": ["${workspaceFolder}/utils/build_script.py"],
              "presentation": {
                "reveal": "always",
                "panel": "new"
              }
            },
            {
              "label": "Push to PyPi",
              "type": "shell",
              "command": "python",
                "args": [
                  "${workspaceFolder}/utils/push_script.py",
                  "--deploy",
                  "True",
                  "--test",
                  "False",
                  "--reformat",
                  "False",
                  "--version",
                  "--commit_and_push_git",
                  "False",
                  "--sphinx_docs",
                  "False"
                ],
                "presentation": {
                  "reveal": "always",
                  "panel": "new"
              }
            },
            {
              "label": "Hooks & push & deploy",
              "type": "shell",
              "command": "python",
              "args": [
                "${workspaceFolder}/utils/push_script.py",
                "--version",
                "${input:version}",
                "--commit_message",
                "${input:commit_message}",
                "--tag",
                "${input:tag}",
                "--tag_mesage",
                "${input:tag-message}"
              ],
              "presentation": {
                "reveal": "always",
                "panel": "new"
              }
            }
          ],
          "inputs": [
            {
              "type": "promptString",
              "id": "version",
              "description": "Version in __init__.py will be overwiten. Version has to be in format like '1.0.3' three digits and two dots. If None, nothing will happen. If 'increment', than it will be updated by 0.0.1.",
              "default": "increment"
            },
            {
              "type": "promptString",
              "id": "commit_message",
              "description": "Git message for commit.",
              "default": "New commit"
            },
            {
              "type": "promptString",
              "id": "tag",
              "description": "Git tag. If '__version__' is used, then tag from version in __init__.py will be derived. E.g. 'v1.0.1' from '1.0.1'",
              "default": "__version__"
            },
            {
              "type": "promptString",
              "id": "tag-message",
              "description": "Git tag message.",
              "default": "New version"
            }
          ]
        }


    **Git hooks example**

    Create folder git_hooks with git hook file - for pre commit name must be `pre-commit`
    (with no extension). Hooks in git folder are gitignored by default (and hooks is not visible
    on first sight).

    Then add hook to git settings - run in terminal (last arg is path (created folder))::

        $ git config core.hooksPath git_hooks

    In created folder on first two lines copy this::

        #!/usr/bin/env python
        # -*- coding: UTF-8 -*-

    Then just import any function from here and call with desired params. E.g.
"""

from __future__ import annotations
import argparse
import ast
import importlib.util
from pathlib import Path
import subprocess
import sys
import os
import importlib

import mylogging

from .misc import get_console_str_with_quotes, str_to_bool, GLOBAL_VARS
from . import tests
from . import deploy as deploy_module
from .paths import PROJECT_PATHS, validate_path

# Lazy loaded
# from git import Repo
# import json


def push_pipeline(
    reformat: bool = True,
    test: bool = True,
    test_options: dict = {},
    version: str = "increment",
    sphinx_docs: bool | list[str] = True,
    commit_and_push_git: bool = True,
    commit_message: str = "New commit",
    tag: str = "__version__",
    tag_mesage: str = "New version",
    deploy: bool = False,
    allowed_branches: list[str] = ["master", "main"],
) -> None:
    """Run pipeline for pushing and deploying app. Can run tests, generate rst files for sphinx docs,
    push to github and deploy to pypi. All params can be configured not only with function params,
    but also from command line with params and therefore callable from terminal and optimal to run
    from IDE (for example with creating simple VS Code task).

    Some function suppose some project structure (where are the docs, where is __init__.py etc.).
    If you are issuing some error, try functions directly, find necessary paths in parameters
    and set paths that are necessary in paths module.

    Note:
        Beware that pushing to git create a commit and add all the changes.

    Check utils module docs for implementation example.

    Args:
        reformat (bool, optional): Reformat all python files with black. Setup parameters in
            `pyproject.toml`, especially setup `line-length`. Defaults to True.
        test (bool, optional): Whether run pytest tests. Defaults to True.
        test_options (dict, optional): Parameters of tests function e.g.
            `{"test_coverage": True, "verbose": False, "use_virutalenv":True}`. Defaults to {}.
        version (str, optional): New version. E.g. '1.2.5'. If 'increment', than it's auto
            incremented. E.g from '1.0.2' to 'v1.0.3'. If empty string "" or not value arg in CLI,
            then version is not changed. 'Defaults to "increment".
        sphinx_docs(bool | list[str], optional): Whether generate sphinx apidoc and generate rst
            files for documentation. Some files in docs source can be deleted - check `sphinx_docs`
            docstrings for details and insert `exclude_paths` list if have some extra files other
            than ['conf.py', 'index.rst', '_static', '_templates']. Defaults to True.
        commit_and_push_git (bool, optional): Whether push repository on git with git_message, tag and tag
            message. Defaults to True.
        git_message (str, optional): Git message. Defaults to 'New commit'.
        tag (str, optional): Used tag. If tag is '__version__', than updated version from __init__
            is used.  If empty string "" or not value arg in CLI, then tag is not created.
            Defaults to __version__.
        tag_mesage (str, optional): Tag message. Defaults to New version.
        deploy (bool, optional): Whether deploy to PYPI. `TWINE_USERNAME` and `TWINE_PASSWORD`
            are used for authorization. Defaults to False.
        allowed_branches (list[str], optional): As there are stages like pushing to git or to PyPi,
            it's better to secure it to not to be triggered on some feature branch. If not one of
            defined branches, error is raised. Defaults to ["master", "main"].

    Example:
        Recommended use is from IDE (for example with Tasks in VS Code). Check utils docs for how
        to use it. You can also use it from python...

        Put it in `if __name__ == "__main__":` block

        >>> push_pipeline(commit_and_push_git=False, deploy=False)

        It's also possible to use CLI and configure it via args. This example just push repo to PyPi.

            python path-to-project/utils/push_script.py --deploy True --test False --reformat False --version --push_git False --sphinx_docs False
    """
    if allowed_branches and not GLOBAL_VARS.IS_TESTED:
        import git.repo

        branch = git.repo.Repo(PROJECT_PATHS.ROOT_PATH.as_posix()).active_branch.name

        if branch not in allowed_branches:
            raise RuntimeError(
                mylogging.critical(
                    (
                        "Pipeline started on branch that is not allowed."
                        "If you want to use it anyway, add it to allowed_branches parameter and "
                        "turn off changing version and creating tag."
                    ),
                    caption="Pipeline error",
                )
            )

    config = {
        "reformat": reformat,
        "test": test,
        "test_options": test_options,
        "version": version,
        "sphinx_docs": sphinx_docs,
        "commit_and_push_git": commit_and_push_git,
        "commit_message": commit_message,
        "tag": tag,
        "tag_mesage": tag_mesage,
        "deploy": deploy,
    }

    # Todo check if there is some arg that is not understood and raise
    if len(sys.argv) > 1 and not GLOBAL_VARS.IS_TESTED:
        parser = argparse.ArgumentParser(description="Prediction framework setting via command line parser!")

        parser.add_argument(
            "--reformat",
            choices=(True, False),
            type=str_to_bool,
            nargs="?",
            help=(
                "Whether reformat all python files with black. Setup parameters in pyproject.toml. Defaults to True."
            ),
        )
        parser.add_argument(
            "--test",
            choices=(True, False),
            type=str_to_bool,
            nargs="?",
            help=("Whether run pytest. Defaults to: True."),
        )
        parser.add_argument(
            "--test_options",
            type=str,
            help=(
                "Check tests module and function run_tests for what parameters you can use. Defaults to: {}."
            ),
        )
        parser.add_argument(
            "--version",
            type=str,
            help=(
                "Version in __init__.py will be overwritten. Version has to be in format like '1.0.3' three digits"
                "and two dots. If None, nothing will happen. If 'increment', than it will be updated by 0.0.1."
                "Defaults to: 'increment'."
            ),
            nargs="?",
            const="",
        )
        parser.add_argument(
            "--sphinx_docs",
            choices=(True, False),
            type=str_to_bool,
            nargs="?",
            help=("Whether run apidoc to create files for example for readthedocs. Defaults to: True."),
        )
        parser.add_argument(
            "--commit_and_push_git",
            choices=(True, False),
            type=str_to_bool,
            nargs="?",
            help=("Whether push to github or not. Defaults to: True."),
        )
        parser.add_argument(
            "--commit_message", type=str, help="Commit message. Defaults to: 'New commit'.",
        )
        parser.add_argument(
            "--tag",
            type=str,
            help="Tag. E.g 'v1.1.2'. If '__version__', get the version. Defaults to: '__version__'.",
            nargs="?",
            const="",
        )
        parser.add_argument(
            "--tag_mesage", type=str, help="Tag message. Defaults to: 'New version'.",
        )
        parser.add_argument(
            "--deploy",
            choices=(True, False),
            type=str_to_bool,
            nargs="?",
            help=(
                "Whether deploy to PYPI. `TWINE_USERNAME` and `TWINE_PASSWORD` "
                "are used for authorization. Defaults to False."
            ),
        )
        parser_args = parser.parse_args()
        parser_args_dict = {i: j for i, j in vars(parser_args).items() if j}

        if parser_args_dict:
            config.update(parser_args_dict)

    # Do some checks before run pipeline so not need to rollback eventually
    if config["deploy"]:
        usr = os.environ.get("TWINE_USERNAME")
        pas = os.environ.get("TWINE_PASSWORD")

        if not usr or not pas:
            raise KeyError(
                mylogging.return_str("Setup env vars TWINE_USERNAME and TWINE_PASSWORD to use deploy.")
            )

    if config["reformat"]:
        reformat_with_black()

    if config["test"]:
        if isinstance(config["test_options"], str):
            import json

            config["test_options"] = json.loads(config["test_options"])

        tests.run_tests(**test_options)

    if config["version"]:
        original_version = get_version()
        set_version(config["version"])

    try:
        if isinstance(config["sphinx_docs"], list):
            sphinx_docs_regenerate(exclude_paths=config["sphinx_docs"])
        elif config["sphinx_docs"]:
            sphinx_docs_regenerate()

        if config["commit_and_push_git"]:
            git_push(
                commit_message=config["commit_message"], tag=config["tag"], tag_message=config["tag_mesage"],
            )
    except Exception:
        if config["version"]:
            set_version(original_version)

        mylogging.traceback(
            "Utils pipeline failed. Original version restored. Nothing was pushed to repo, you can restart pipeline."
        )
        return

    try:
        if config["deploy"]:
            deploy_module.deploy_to_pypi()
    except Exception:
        mylogging.traceback(
            "Deploy failed, but pushed to repository already. Deploy manually. Version already changed.",
            level="CRITICAL",
        )


def reformat_with_black(root_path: str | Path = "infer", extra_args: list[str] = ["--quiet"]) -> None:
    """Reformat code with black.

    Args:
        root_path (str | Path, optional): Root path of project. Defaults to "infer".
        extra_args (list[str], optional): Some extra args for black. Defaults to ["--quiet"].

    Example:
        >>> reformat_with_black()
    """
    root_path = PROJECT_PATHS.ROOT_PATH if root_path == "infer" else validate_path(root_path)

    try:
        subprocess.run(f"black . {' '.join(extra_args)}", check=True, cwd=root_path)
    except FileNotFoundError:
        mylogging.traceback(
            "FileNotFoundError can happen if `black` is not installed. Check it with pip list in used python interpreter."
        )
        raise
    except (Exception,):
        mylogging.traceback(
            "Reformatting with `black` failed. Check if it's installed, check logged error, "
            "then try format manually with \n\nblack .\n\n"
        )
        raise


def git_push(commit_message: str, tag: str = "__version__", tag_message: str = "New version",) -> None:
    """Stage all changes, commit, add tag and push. If tag = '__version__', than tag
    is inferred from __init__.py.

    Args:
        commit_message (str): Commit message.
        tag (str, optional): Define tag used in push. If tag is '__version__', than is automatically generated
            from __init__ version. E.g from '1.0.2' to 'v1.0.2'.  Defaults to '__version__'.
        tag_message (str, optional): Message in annotated tag. Defaults to 'New version'.
    """

    import git.repo

    git_command = f"git add . && git commit -m {get_console_str_with_quotes(commit_message)} && git push"

    if tag == "__version__":
        tag = f"v{get_version()}"

    if tag:
        if not tag_message:
            tag_message = "New version"

        git.repo.Repo(PROJECT_PATHS.ROOT_PATH.as_posix()).create_tag(tag, message=tag_message)
        git_command += " --follow-tags"

    try:
        subprocess.run(git_command, check=True, cwd=PROJECT_PATHS.ROOT_PATH.as_posix(), shell=True)
    except (Exception,):
        git.repo.Repo(PROJECT_PATHS.ROOT_PATH.as_posix()).delete_tag(tag)
        mylogging.traceback(
            "Push to git failed. Version restored and created git tag deleted."
            f"Try to run command \n\n{git_command}\n\n manually in your root {PROJECT_PATHS.ROOT_PATH}."
        )
        raise


def set_version(version: str = "increment", init_path: str | Path = "infer",) -> None:
    """Change your version in your __init__.py file.


    Args:
        version (str, optional): Form that is used in __init__, so for example "1.2.3". Do not use 'v' appendix.
            If version is 'increment', it will increment your __version__ in you __init__.py by 0.0.1. Defaults to "increment".
        init_path (str | Path, optional): Path of file where __version__ is defined. Usually __init__.py, Defaults to "infer".

    Raises:
        ValueError: If no __version__ is find.
    """

    init_path = PROJECT_PATHS.INIT_PATH if init_path == "infer" else validate_path(init_path)

    if version == "increment" or (
        len(version.split(".")) == 3 and all([i.isdecimal() for i in version.split(".")])
    ):
        pass

    else:
        raise ValueError(
            mylogging.return_str(
                f"Version not validated. Version has to be of form '1.2.3'. Three digits and two dots. You used {version}"
            )
        )

    with open(init_path.as_posix(), "r") as init_file:

        list_of_lines = init_file.readlines()

        for i, j in enumerate(list_of_lines):
            if j.startswith("__version__"):

                found = True

                delimiter = '"' if '"' in j else "'"
                delimited = j.split(delimiter)

                if version == "increment":
                    version_list = delimited[1].split(".")
                    version_list[2] = str(int(version_list[2]) + 1)
                    delimited[1] = ".".join(version_list)

                else:
                    delimited[1] = version

                list_of_lines[i] = delimiter.join(delimited)
                break

        if not found:
            raise ValueError(
                mylogging.return_str("__version__ variable not found in __init__.py. Try set INIT_PATH.")
            )

    with open(init_path.as_posix(), "w") as init_file:

        init_file.writelines(list_of_lines)


def get_version(init_path: str | Path = "infer") -> str:
    """Get version info from __init__.py file.

    Args:
        init_path (str | Path, optional): Path to __init__.py file. Defaults to "infer".

    Returns:
        str: String of version from __init__.py.

    Raises:
        ValueError: If no __version__ is find. Try set init_path...

    Example:
        >>> version = get_version()
        >>> len(version.split(".")) == 3 and all([i.isdecimal() for i in version.split(".")])
        True
    """

    init_path = PROJECT_PATHS.INIT_PATH if init_path == "infer" else validate_path(init_path)

    with open(init_path.as_posix(), "r") as init_file:

        for line in init_file:

            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]

        else:
            raise ValueError(mylogging.return_str("__version__ variable not found in __init__.py."))


def sphinx_docs_regenerate(
    docs_path: str | Path = "infer",
    build_locally: bool = False,
    git_add: bool = True,
    exclude_paths: list[str | Path] = [],
    delete: list[str | Path] = ["modules.rst"],
) -> None:
    """This will generate all rst files necessary for sphinx documentation generation with sphinx-apidoc.
    It automatically delete removed and renamed files.

    Note:
        All the files except ['conf.py', 'index.rst', '_static', '_templates'] will be deleted!!!
        Because if some files would be deleted or renamed, rst would stay and html was generated.
        If you have some extra files or folders in docs source - add it to `exclude_paths` list.

    Function suppose sphinx build and source in separate folders...

    Args:
        docs_path (str | Path, optional): Where source folder is. Usually inferred automatically.
            Defaults to "infer".
        build_locally (bool, optional): If true, build folder with html files locally.
            Defaults to False.
        git_add (bool, optional): Whether to add generated files to stage. False mostly for
            testing reasons. Defaults to True.
        exclude_paths (list[str | Path], optional): List of files and folder names that will not be deleted.
            ['conf.py', 'index.rst', '_static', '_templates'] are excluded by default. Defaults to [].
        delete (list[str | Path], optional): If delete some files (for example to have no errors in sphinx build for unused modules)

    Note:
        Function suppose structure of docs like::

            -- docs
            -- -- source
            -- -- -- conf.py
            -- -- make.bat
    """

    if not importlib.util.find_spec("sphinx"):
        raise ImportError(
            mylogging.return_str(
                "Sphinx library is necessary for docs generation. Install via \n\npip install sphinx\n\n"
            )
        )

    docs_path = PROJECT_PATHS.DOCS_PATH if docs_path == "infer" else validate_path(docs_path)

    docs_source_path = Path(docs_path).resolve() / "source"

    for p in docs_source_path.iterdir():
        if p.name not in [
            "conf.py",
            "index.rst",
            "_static",
            "_templates",
            *exclude_paths,
        ]:
            try:
                p.unlink()
            except Exception:
                pass

    apidoc_command = f"sphinx-apidoc -f -e -o source {get_console_str_with_quotes(PROJECT_PATHS.APP_PATH)}"
    subprocess.run(
        apidoc_command, cwd=docs_path, check=True,
    )

    if delete:
        for i in delete:
            (docs_source_path / i).unlink()

    if build_locally:
        subprocess.run(["make", "html"], cwd=docs_path, check=True)

    if git_add:
        subprocess.run(
            ["git", "add", "docs"], cwd=PROJECT_PATHS.ROOT_PATH.as_posix(), check=True,
        )


def generate_readme_from_init(git_add: bool = True) -> None:
    """Because i had very similar things in main __init__.py and in readme. It was to maintain news
    in code. For better simplicity i prefer write docs once and then generate. One code, two use cases.

    Why __init__? - Because in IDE on mouseover developers can see help.
    Why README.md? - Good for github.com

    Args:
        git_add (bool, optional): Whether to add generated files to stage. False mostly
            for testing reasons. Defaults to True.
    """

    with open(PROJECT_PATHS.INIT_PATH.as_posix()) as fd:
        file_contents = fd.read()
    module = ast.parse(file_contents)
    docstrings = ast.get_docstring(module)

    if docstrings is None:
        docstrings = ""

    with open(PROJECT_PATHS.README_PATH.as_posix(), "w") as file:
        file.write(docstrings)

    if git_add:
        subprocess.run(
            ["git", "add", PROJECT_PATHS.README_PATH,], cwd=PROJECT_PATHS.ROOT_PATH.as_posix(), check=True,
        )
