#%%
import shutil
from pathlib import Path
import sys
import os

root_path = Path(__file__).parents[1].as_posix()
sys.path.insert(0, root_path)

import mypythontools

test_project_path = Path("tests").resolve() / "tested_project"


def test_paths():

    assert mypythontools.paths.PROJECT_PATHS.ROOT_PATH == test_project_path
    assert mypythontools.paths.PROJECT_PATHS.INIT_PATH == test_project_path / "project_lib" / "__init__.py"
    assert mypythontools.paths.PROJECT_PATHS.APP_PATH == test_project_path / "project_lib"
    assert mypythontools.paths.PROJECT_PATHS.DOCS_PATH == test_project_path / "docs"
    assert mypythontools.paths.PROJECT_PATHS.README_PATH == test_project_path / "README.md"
    assert mypythontools.paths.PROJECT_PATHS.TEST_PATH == test_project_path / "tests"


def test_utils():

    rst_path = test_project_path / "docs" / "source" / "project_lib.rst"
    not_deleted = test_project_path / "docs" / "source" / "not_deleted.rst"

    if rst_path.exists():
        rst_path.unlink()  # missing_ok=True from python 3.8 on...

    if not not_deleted.exists():
        with open(not_deleted, "w") as not_deleted_file:
            not_deleted_file.write("I will not be deleted.")
            # missing_ok=True from python 3.8 on...

    mypythontools.utils.sphinx_docs_regenerate(exclude_paths=["not_deleted.rst"])

    mypythontools.utils.reformat_with_black()

    assert rst_path.exists()
    assert not_deleted.exists()

    mypythontools.utils.set_version("0.0.2")
    assert mypythontools.utils.get_version() == "0.0.2"
    mypythontools.utils.set_version("0.0.1")

    # TODO test if correct


def test_build():

    # Build app with pyinstaller example
    mypythontools.build.build_app(
        main_file="app.py",
        console=True,
        debug=True,
        cleanit=False,
        build_web=False,
        ignored_packages=["matplotlib"],
    )

    assert (test_project_path / "dist").exists()

    shutil.rmtree(test_project_path / "build")
    shutil.rmtree(test_project_path / "dist")


def test_config_argparse():
    """Doctest not tested in config. If changing test, change docs as well."""

    import subprocess

    int_arg = subprocess.check_output(
        "python tests/test_argparse.py --int_arg 666", cwd=root_path, text=True
    ).strip()
    float_arg = subprocess.check_output(
        "python tests/test_argparse.py --float_arg 666", cwd=root_path, text=True
    ).strip()
    str_arg = subprocess.check_output(
        "python tests/test_argparse.py --str_arg 666", cwd=root_path, text=True
    ).strip()
    list_arg = subprocess.check_output(
        "python tests/test_argparse.py --list_arg [666]", cwd=root_path, text=True
    ).strip()
    dict_arg = subprocess.check_output(
        """python tests/test_argparse.py --dict_arg "{'key': 666}" """, cwd=root_path, text=True
    ).strip()

    get_help = subprocess.check_output(
        "python tests/test_argparse.py --help", cwd=root_path, text=True
    ).strip()

    for i in ["int_arg", "666", "int"]:
        assert i in int_arg
    for i in ["float_arg", "666", "float"]:
        assert i in float_arg
    for i in ["str_arg", "666", "str"]:
        assert i in str_arg
    for i in ["list_arg", "666", "list"]:
        assert i in list_arg
    for i in ["dict_arg", "666", "dict"]:
        assert i in dict_arg

    assert "This should be in CLI help" in get_help and "How it works." in get_help


if __name__ == "__main__":
    # Find paths and add to sys.path to be able to import local modules
    mypythontools.tests.setup_tests()

    test_project_path = Path("tests").resolve() / "tested_project"
    os.chdir(test_project_path)
    mypythontools.paths.PROJECT_PATHS = mypythontools.paths._ProjectPaths()

    # test_paths()

    test_config_argparse()
