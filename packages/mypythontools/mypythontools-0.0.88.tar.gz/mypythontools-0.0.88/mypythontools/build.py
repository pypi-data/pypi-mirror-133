"""
This module build the app via pyinstaller.
It has presets to build applications build with eel.

There is one main function `build_app`. Check it's help for how to use
it (should be very simple).

Note:
    You can run build for example from vs code tasks, create folder utils,
    create build_script.py inside, add

    >>> import mypythontools
    ...
    >>> if __name__ == "__main__":
    ...     mypythontools.build.build_app()  # With all the params you need.

    Then just add this task to global tasks.json::

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
"""

from __future__ import annotations
import subprocess
import shutil
from pathlib import Path
import mylogging
import sys

from typing_extensions import Literal

# Lazy imports
# import EelForkExcludeFiles

from . import paths
from . import venvs
from .paths import PROJECT_PATHS


def build_app(
    root_path: str | Path = "infer",
    main_file: str | Path = "app.py",
    preset: Literal["eel", None] = None,
    web_path: str | Path | None = "infer",
    build_web: bool | str = "preset",
    use_virutalenv: bool = True,
    remove_last_build: bool = False,
    console: bool = True,
    debug: bool = False,
    icon: str | Path | None = None,
    hidden_imports: list[str] = [],
    ignored_packages: list[str] = [],
    datas: tuple[tuple[str, str], ...] = (),
    name: str = None,
    env_vars: dict = {},
    cleanit: bool = True,
) -> None:
    """One script to build .exe app from source code.

        This script automatically generate .spec file, build node web files and add environment variables during build.

        This script suppose some structure of the app (may have way different though). You can use project-starter from the same repository,
        if you start with application.

        Args:
            root_path (str | Path, optional): Path of root folder where build and dist folders will be placed. Defaults to "infer".
            main_file (str, optional): Main file path or name with extension. Main file is found automatically
                and don't have to be in root. Defaults to 'app.py'.
            preset (Literal['eel', None], optional): Edit other params for specific use cases (append to hidden_imports, datas etc.).
                Defaults to None.
            web_path (str | Path | None, optional): Folder with index.html. Defaults to 'infer'.
            build_web (bool | str, optional): If application contain package.json build node application. If 'preset' build automatically
                depending on preset. Defaults to 'preset'.
            use_virutalenv (bool, optional): Whether run new virtualenv and install all libraries from requirements.txt. Defaults to True.
            remove_last_build (bool, optional): If some problems, it is possible to delete build and dist folders. Defaults to False.
            console (bool, optional): Before app run terminal window appears (good for debugging). Defaults to False.
            debug (bool, optional): If no console, then dialog window with traceback appears. Defaults to False.
            icon (str | Path | None, optional): Path or name with extension to .ico file (!no png!). Defaults to None.
            hidden_imports (list, optional): If app is not working, it can be because some library was not builded. Add such
                libraries into this list. Defaults to [].
            ignored_packages (list, optional): Libraries take space even if not necessary. Defaults to [].
            datas (tuple[tuple[str, str], ...], optional): Add static files to build. Example: [('my_source_path, 'destination_path')]. Defaults to [].
            name (str, optional): If name of app is different than main py file. Defaults to None.
            env_vars (dict, optional): Add some env vars during build. Mostly to tell main script that it's production (ne development) mode.
                Defaults to {}.
            cleanit (bool, optional): Remove spec file and var env py hook. Defaults to True.

        Note:
            Build pyinstaller bootloader on your pc, otherwise antivirus can check the
            file for a while on first run and even alert false positive.

            Download from github, cd to bootloader and::
    +
                python ./waf all

            Back to pyinstaller folder and python `setup.py`
    """

    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        raise RuntimeError(mylogging.return_str("Python version >=3.10 not supported yet."))

    root_path = PROJECT_PATHS.ROOT_PATH if root_path == "infer" else paths.validate_path(root_path)

    # Try to recognize the structure of app
    build_path = root_path / "build"

    if not build_path.exists():
        build_path.mkdir(parents=True, exist_ok=True)

    # Remove last dist manually to avoid permission error if opened in some application
    dist_path = root_path / "dist"

    if dist_path.exists():
        try:
            shutil.rmtree(dist_path, ignore_errors=False)
        except (PermissionError, OSError):

            raise PermissionError(
                mylogging.return_str(
                    "App is opened (May be in another app(terminal, explorer...)). Close it first."
                )
            )

    # May be just name - not absolute
    main_file_path = Path(main_file)

    if not main_file_path.exists():

        # Iter paths and find the one
        main_file_path = paths.find_path(main_file_path.name,)

        if not main_file_path.exists():
            raise KeyError("Main file not found, not inferred and must be configured in params...")

    main_file_path = main_file_path.resolve()

    if not name:
        name = main_file_path.stem

    main_folder_path = main_file_path.parent

    if icon:
        icon_path = Path(icon)

        if not icon_path.exists():

            # Iter paths and find the one
            icon_path = paths.find_path(icon_path.name, exclude_names=["node_modules", "build"],)

            if not icon_path.exists():
                raise KeyError("Icon not found, not inferred check path or name...")
    else:
        icon_path = None

    generated_warning = """
#########################
### File is generated ###
#########################

# Do not edit this file, edit build_script
"""

    if remove_last_build:
        try:
            shutil.rmtree("build", ignore_errors=True)
        except Exception:
            pass

    # Build JS to static asset
    if build_web is True or (build_web == "preset" and preset in ["eel"]):
        gui_path = paths.find_path("package.json").parent
        try:
            builded = subprocess.run("npm run build", check=True, cwd=gui_path.as_posix(), shell=True)
            if builded.returncode != 0:
                raise RuntimeError()

        except Exception:
            mylogging.traceback(f"Build of web files failed. Try \n\nnpm run build\n\n in folder {gui_path}.")
            raise

    if build_web or preset == "eel":
        if web_path == "infer":
            web_path = paths.find_path(
                "index.html", exclude_names=["public", "node_modules", "build",],
            ).parent

        else:
            web_path = Path(web_path)

        if not web_path.exists():
            raise KeyError("Build web assets not found, not inferred and must be configured in params...")

        datas = (
            *datas,
            (web_path.as_posix(), "gui"),
        )

    if preset == "eel":

        import EelForkExcludeFiles

        hidden_imports = [
            *hidden_imports,
            "EelForkExcludeFiles",
            "bottle_websocket",
        ]
        datas = (
            *datas,
            (EelForkExcludeFiles._eel_js_file, "EelForkExcludeFiles",),
        )
        env_vars = {
            **env_vars,
            "MY_PYTHON_VUE_ENVIRONMENT": "production",
        }

    if env_vars:
        env_vars_template = f"""
{generated_warning}

import os
for i, j in {env_vars}.items():
    os.environ[i] = j
"""

        env_path = build_path / "env_vars.py"

        with open(env_path, "w") as env_vars_py:
            env_vars_py.write(env_vars_template)
        runtime_hooks = [env_path.as_posix()]
    else:
        runtime_hooks = None

    spec_template = f"""
{generated_warning}

import sys
from pathlib import Path
import os

sys.setrecursionlimit(5000)
block_cipher = None

a = Analysis(['{main_file_path.as_posix()}'],
            pathex=['{main_folder_path.as_posix()}'],
            binaries=[],
            datas={datas},
            hiddenimports={hidden_imports},
            hookspath=[],
            runtime_hooks={runtime_hooks},
            excludes={ignored_packages},
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='{name}',
        debug={debug},
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console={console},
        icon={f"'{icon_path.as_posix()}'" if icon else None})
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='{name}')
"""
    spec_path = build_path / "app.spec"

    with open(spec_path, "w") as spec_file:
        spec_file.write(spec_template)

    # Build py to exe
    command_list = ["pyinstaller", "-y", spec_path.as_posix()]

    if use_virutalenv:
        my_venv = venvs.MyVenv(PROJECT_PATHS.ROOT_PATH / "venv")
        my_venv.create()
        my_venv.sync_requirements()

        command_list = [*my_venv.activate_command.split(), " && ", *command_list]

    try:
        subprocess.run(" ".join(command_list), check=True, cwd=PROJECT_PATHS.ROOT_PATH.as_posix(), shell=True)

    except (Exception,):
        mylogging.traceback(
            "Build with pyinstaller failed. First, check if `pyinstaller` is installed. Check it with pip list in used python interpreter. "
            f" Try (if windows, use cmd) \n\n\t{' '.join(command_list)}\n\n in folder `{PROJECT_PATHS.ROOT_PATH.as_posix()}`.\n\n"
            "Troubleshooting: If there are still errors, try to install newset pyinstaller locally with `python setup.py install`, "
            "update setuptools, delete `build` and `dist` folder and try again."
        )
        raise

    if cleanit:
        try:
            spec_path.unlink()
            env_path.unlink()
        except Exception:
            pass
