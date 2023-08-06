"""
Inferring how to launch a project.
"""
import ast
import os
import re
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path
from textwrap import dedent
from typing import List, Optional

import requests

from jaepeto.utils import post


class PyVersionDetector:
    def __init__(self):
        self._version_reason = []

        self.PY35 = 35
        self.PY36 = 36
        self.PY37 = 37
        self.PY38 = 38
        self.PY39 = 39
        self.PY310 = 310
        self._version = None
        self.possible_versions = (
            self.PY36,
            self.PY37,
            self.PY38,
            self.PY39,
            self.PY310,
        )

        subscript_type_pattern = r"\[\w+:?\s?\w+\]"
        type_hint_pattern = rf"\s?\w+(?:{subscript_type_pattern})?\s?"
        assignment_pattern = rf"\w+\s?(?::{type_hint_pattern})?=\s?"

        # 3.6
        self._f_string_36 = []
        self._f_string_pattern = re.compile(r"fr?['\"](.*)[\'\"]", re.IGNORECASE)

        # 3.8
        self._walrus = []
        self._walrus_pattern = re.compile(r"if\s\(?\w*\s?:=\s?.+\)?")
        self._f_string_38 = []

        # 3.9
        self._dict_union = []
        self._dict_union_pattern = re.compile(
            rf"^[^'\"]*?(?:(?:[,\(]\s?)|(?:{assignment_pattern}))\w+\s?\|\s?\w+"
        )

        # 3.10
        self._pipe_optional = []
        self._pipe_pattern = re.compile(
            rf"^[^'\"].*?\w+ ?:{type_hint_pattern}\|{type_hint_pattern}[,\)=]"
        )

        self._type_hint = []
        self._match_operator = []

    @property
    def version(self) -> str:
        _ver = str(self._version) if self._version else str(self.PY37)
        _ver = _ver[0] + "." + _ver[1:]
        return _ver

    def has_fstring(self, code, filename) -> bool:
        return False
        # TODO: fix this method
        tree = ast.parse(code, filename)
        for node in ast.walk(tree):
            if isinstance(node, ast.JoinedStr):
                return any(
                    [
                        isinstance(value, ast.Constant) and "=" in value.value
                        for value in node.values
                    ]
                )

    def review(self, filename: str, code_contents: List[str]) -> None:
        __version = self.PY35 if not self._version else self._version

        for considered_version in self.possible_versions:
            if considered_version <= __version:
                continue

            if considered_version == self.PY36:
                self._match_36(filename, code_contents)
            elif considered_version == self.PY38:
                self._match_38(filename, code_contents)
            elif considered_version == self.PY39:
                self._match_39(filename, code_contents)
            elif considered_version == self.PY310:
                self._match_310(filename, code_contents)

    def _match_36(self, filename: str, code_contents: List[str]) -> None:
        for _code in code_contents:

            _code = _code.strip()
            if pipe_dict := self._f_string_pattern.search(_code):
                if self.has_fstring(_code, filename) == False:
                    self._f_string_36.append(filename)

                    if not self._version or self._version < self.PY36:
                        self._version_reason = []
                        self._version = self.PY36
                    self._version_reason.append(("f-string 3.6", filename))

    def _match_38(self, filename: str, code_contents: List[str]) -> None:
        for _code in code_contents:
            _code = _code.strip()
            if walrus := self._walrus_pattern.search(_code):
                self._walrus.append(filename)

                if not self._version or self._version < self.PY38:
                    self._version_reason = []
                    self._version = self.PY38
                self._version_reason.append(("walrus", filename))
            elif f_string := self._f_string_pattern.search(_code):
                if self.has_fstring(_code, filename):
                    self._f_string_38.append(filename)

                    if not self._version or self._version < self.PY38:
                        self._version_reason = []
                        self._version = self.PY38
                    self._version_reason.append(("f-string 3.8", filename))

    def _match_39(self, filename: str, code_contents: List[str]) -> None:
        for _code in code_contents:
            _code = _code.strip()
            if pipe_dict := self._dict_union_pattern.search(_code):
                self._dict_union.append(filename)

                if not self._version or self._version < self.PY39:
                    self._version_reason = []
                    self._version = self.PY39
                self._version_reason.append(("pipe dictionary union", filename))

    def _match_310(self, filename: str, code_contents: List[str]) -> None:
        for _code in code_contents:
            _code = _code.strip()
            if pipe := self._pipe_pattern.search(_code):
                self._pipe_optional.append(filename)

                if not self._version or self._version < self.PY310:
                    self._version_reason = []
                    self._version = self.PY310
                self._version_reason.append(("pipe type hint", filename))

    def __str__(self):
        if not self._version:
            return dedent(
                """
                    No exact compatable Python version has been detected.
                    Versions below 3.8 are compatable.
                    """
            )
        else:
            ver_str = f"The codebase is compatible with Python {self.version} and above, because of {self._version_reason[0][0]} in {self._version_reason[0][1]}."
            return ver_str


class SetupParser:
    def __init__(self) -> None:
        self.is_package = False
        self.pypi_package = None
        self.cli = {}

    def parse(self, project_dir: Path, package_name: Optional[str]) -> None:
        if (setup_py := (project_dir / "setup.py")).exists():
            self.is_package = True
            self.parse_setup(setup_py, setup_type="py")

        if (setup_cfg := (project_dir / "setup.cfg")).exists():
            self.is_package = True
            self.parse_setup(setup_cfg, setup_type="cfg")

        self._check_pypi(package_name)

    def parse_setup(self, file: Path, /, *, setup_type: str) -> None:
        with open(file, "r") as f:
            contents = f.read()

        if response := post(f"setup/{setup_type}", contents):
            if isinstance(response, list):
                for _key, _value in response:
                    self.cli[_key] = _value

    def _check_pypi(self, package_name: Optional[str]) -> None:
        """
        Check pypi to infer if package is globally pip-installable.

        Uses `requests` to look for the package on pypi.
        If present on pypi, assumes that that is the correct package.
        **Note:** This may lead to a false positive if the package shares
        a name with a project already on pypi.

        Parameters
        ----------
        package_name : str or None
            The local pip-installable package name for the codebase, if codebase is installable.
            Otherwise None.

        Notes
        -----
        * `pip search` has been taken down. If it resurfaces, that would be a more applicable check.
        """
        if package_name:
            if (
                requests.get(f"https://pypi.org/project/{package_name}/").status_code
                == 200
            ):
                self.pypi_package = package_name

    def __str__(self) -> str:
        setup_string = ""

        if self.is_package:
            setup_string += dedent(
                """
                Run `pip install -e .` in top-level directory to install
                package in local directory.
                """
            )

        if self.pypi_package:
            setup_string += f"Install from pypi with `pip install {self.pypi_package}`."

        return setup_string

    def read_entrypoints(self) -> str:
        description = ""

        cli_desc = ""
        for _command, _func in self.cli.items():
            cli_desc += f"* `{_command}` runs `{_func}`\n"

        if cli_desc:
            cli_desc = (
                "The project has the following CLI commands:\n\n" + cli_desc + "\n"
            )
            cli_desc += "Run a CLI command in a terminal to execute."
            description += cli_desc

        return description


class OnboardingParser:
    def __init__(self) -> None:
        self._version = PyVersionDetector()
        self._setup = SetupParser()

        self._reqs = False

    def parse(
        self, source_dir: Path, project_dir: Path, package_name: Optional[str] = None
    ) -> None:
        """
        Search a project codebase for "Getting Started" information for users.

        Relevant information includes minimum Python version
        and installation instructions.

        Parameters
        ----------
        source_dir : pathlib.Path
            Path to the source code directory
        project_dir : pathlib.Path
            Path to the root directory of the codebase being analysed
        package_name: str, optional. Default = None.
            The name of the codebase being analysed as it would be imported
        """
        for pyfile in source_dir.glob("**/*.py"):
            with open(pyfile, "r") as f:
                _pyfile_contents = f.readlines()

            self._version.review(pyfile, _pyfile_contents)
            del _pyfile_contents

        if (project_dir / "requirements.txt").exists():
            self._reqs = True

        self._setup.parse(project_dir, package_name)

    def __str__(self) -> str:
        reqs = str(self._version) + "\n"

        if self._reqs:
            reqs += "Install requirements with `pip install -r requirements.txt`.\n"

        reqs += str(self._setup) + "\n"

        if cli_entrypoints := self._setup.read_entrypoints():
            reqs += f"\n\n **Getting started**\n\n{cli_entrypoints}"

        return reqs


class DevOnboardingParser:
    def __init__(self) -> None:

        self._dev_reqs = False
        self._conda: str = ""
        self._pre_commit = False

        self._test_dir: Optional[str] = None
        self._test_libs: List[str] = []

    def parse(self, project_dir) -> None:
        """
        Search a project codebase for "Getting started" information useful to developers.

        Useful "Getting started" information includes the presence of
        separate developer requirements or setup instructions.

        Notes
        -----
        * Detects use of pre-commit
        * Detects presence of a conda environment
        * Detects presence of separate developer requirements
        * Infers testing environment
        """
        if (dev_reqs_file := (project_dir / "requirements-dev.txt")).exists():
            self._dev_reqs = True
            # TODO parse from API

        for _conda_filetype in ("yml", "yaml"):
            if (
                conda_file := (project_dir / f"environment.{_conda_filetype}")
            ).exists():
                self._parse_conda(conda_file)

        if (project_dir / ".pre-commit-config.yaml").exists():
            self._pre_commit = True

        self._parse_tests(project_dir)

    def _parse_tests(self, project_dir: Path) -> None:
        """
        Infer a test folder and framework.

        Detects "test" or "tests" folder as containing automated tests.
        Makes no distinction between types of tests.
        Infers if pytest or unittest testing frameworks are used.
        Some naive assumptions here.
        We should make the inferences more robust.
        """
        for _test_folder in ("tests", "test"):
            if (project_dir / _test_folder).is_dir():
                self._test_dir = _test_folder
                break

        if self._test_dir:
            for test_file in (project_dir / self._test_dir).glob("**/test_*.py"):
                with open(test_file, "r") as f:
                    test_contents = f.read()

                if "pytest" not in self._test_libs and (
                    "import pytest" in test_contents or "from pytest" in test_contents
                ):
                    self._test_libs.append("pytest")

                if "unittest" not in self._test_libs and (
                    "unittest.main" in test_contents or "TestCase):" in test_contents
                ):
                    self._test_libs.append("unittest")

    def _parse_conda(self, file: Path):
        # TODO
        self._conda = file.name

    def __str__(self) -> str:
        reqs = ""
        req_commands = []

        if self._dev_reqs:
            req_commands.append(
                "Install developer requirements with `pip install -r requirements-dev.txt`"
            )

        if self._conda:
            req_commands.append(
                f"To create an isolated development environment with anaconda, run `conda env create -f {self._conda}`"
            )

        if self._pre_commit:
            req_commands.append(
                "This project uses `pre-commit` to enforce code style on commit. Run `pre-commit install` in a terminal to setup"
            )

        if self._test_dir:
            test_info = f"Tests are present in `{self._test_dir}/`"

            if testing_framework := ", ".join(self._test_libs):
                test_info += f" (using {testing_framework})"

            req_commands.append(test_info)

        if req_commands:
            reqs += "* " + "\n* ".join(req_commands)

        return reqs + "\n\n"
