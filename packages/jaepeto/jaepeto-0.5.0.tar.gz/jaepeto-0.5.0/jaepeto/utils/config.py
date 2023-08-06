"""
Parse user config
"""
import os
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Dict, Optional, Union

import toml
from dotenv import load_dotenv


def _clean_config_dir(value: str) -> str:
    """
    Remove errant / and . from directory values in config.

    Leading `./` and trailing `/`
    are to be removed as the code does not expect paths
    in this format and consequently cannot resolve the paths.

    Parameters
    ----------
    value : str
        The unclean directory

    Returns
    -------
    str
        A clean directory
    """
    value = value.lstrip("./")
    value = value.rstrip("/")
    return value


def parse_jaepeto_ini(config_file: Union[Path, str]) -> Dict:
    config = ConfigParser()
    config.read(config_file)

    project_name = config.get("project", "name")
    project_name = project_name if project_name else "Project"

    src_dir = _clean_config_dir(config.get("project", "srcdir"))
    try:
        package = config.get("project", "package")
    except NoOptionError:
        package = src_dir if "src/" not in src_dir else src_dir.split("src/")[1]

    try:
        description = config.get("project", "description")
    except NoOptionError:
        description = "<SHORT PROJECT DESCRIPTION>"

    project_info = {
        "name": project_name,
        "description": description,
        "src": _clean_config_dir(config.get("project", "srcdir")),
        "doc_dir": _clean_config_dir(config.get("docs", "docdir")),
        "package": package,
    }

    try:
        local = config.getboolean("project", "local")
    except NoOptionError:
        local = False

    try:
        api_key = config.get("project", "api_key")
    except NoOptionError:
        if not os.getenv("JAEPETO_API_KEY"):
            if local:
                print("Using local server.")
            else:
                raise RuntimeError(
                    "No API key detected. Contact `info AT documatic DOT com` to request one."
                )
    else:
        print(
            "Reading api key from config file is DEPRECATED. Place key in `.env` file. See README for more info."
        )
        os.environ["JAEPETO_API_KEY"] = config.get("project", "api_key")

    os.environ["JAEPETO_PROJECT_NAME"] = project_name
    os.environ["JAEPETO_RUN_LOCALLY"] = str(local)

    try:
        language = config.get("project", "language")
    except NoOptionError:
        language = "NoLanguage"

    if language.lower().strip().rstrip("3") != "python":
        print(
            f"""Jaepeto currently only works
        on Python (3), not {language}"""
        )

    # Documentation types
    project_info["docs"] = {
        "technical": True,
        "technical_name": "technical_doc",
        "changelog": "CHANGELOG.md",
    }

    # Documentation settings
    default_settings = {
        "num_class_uses_threshold": 3,
        "max_num_entrypoints_threshold": 10,
    }

    if config.has_section("settings"):
        settings = {}

        for settings_key, default_value in default_settings.items():
            try:
                settings[settings_key] = int(config.get("settings", settings_key))
            except (NoOptionError, ValueError):
                settings[settings_key] = default_value

        project_info["settings"] = settings
    else:
        project_info["settings"] = default_settings

    # Issues
    if config.has_section("issues"):
        issue_service = config.get("issues", "integration")
        if issue_service and issue_service.lower() != "github":
            project_info["issues"] = {}
        else:
            try:
                username = config.get("issues", "username")
                repo = config.get("issues", "repo")
            except:
                project_info["issues"] = {}
            else:
                project_info["issues"] = {"username": username, "repo": repo}
    else:
        project_info["issues"] = {}

    return project_info


def parse_pyproject(config_path: Path) -> Optional[Dict]:
    with open(config_path, "r") as f:
        config_str = f.read()
        config = toml.loads(config_str)

    if "tool" not in config or "jaepeto" not in config["tool"]:
        return None

    jaepeto_config = config["tool"]["jaepeto"]
    project_name = jaepeto_config.get("name")

    if not project_name:
        raise RuntimeError("No 'name' field (project name) in pyproject.toml")

    description = jaepeto_config.get("description", "<SHORT PROJECT DESCRIPTION>")

    srcdir = jaepeto_config.get("srcdir")

    if not srcdir:
        raise RuntimeError("No `srcdir` field (path to source code) in pyproject.toml")

    srcdir = _clean_config_dir(srcdir)

    package = jaepeto_config.get("package", srcdir)
    local = jaepeto_config.get("local", False)
    docdir = _clean_config_dir(jaepeto_config.get("docdir", "."))
    doc_name = jaepeto_config.get("docname", "technical_doc.md")

    if not doc_name.endswith(".md"):
        doc_name += ".md"

    os.environ["JAEPETO_PROJECT_NAME"] = project_name
    os.environ["JAEPETO_RUN_LOCALLY"] = str(local)

    if not os.getenv("JAEPETO_API_KEY"):
        print("No API key detected. Contact `info AT documatic DOT com` to request one")

    project_info = {
        "name": project_name,
        "description": description,
        "src": srcdir,
        "doc_dir": docdir,
        "package": package,
    }

    # Documentation types
    project_info["docs"] = {
        "technical": True,
        "technical_name": doc_name,
        "changelog": "CHANGELOG.md",
    }

    # Documentation settings
    project_info["settings"] = {
        "num_class_uses_threshold": 3,
        "max_num_entrypoints_threshold": 10,
    }

    return project_info


def parse_config(project_root: Path) -> Dict:
    load_dotenv()

    if (ini_path := (project_root / ".jaepeto.ini")).exists():
        return parse_jaepeto_ini(ini_path)
    elif (pyproject_path := project_root / "pyproject.toml").exists():
        project_dir = parse_pyproject(pyproject_path)

        if project_dir:
            return project_dir
        else:
            raise RuntimeError("Invalid config for [tool.jaepeto] in pyproject.toml")
    else:
        raise RuntimeError("No config file detected")


def create_config():
    """
    Create a minimal config file.

    Must be called when project root is current working directory.
    Some information must be filled out by a user, such as `api_key`.
    `srcdir` is assumed to be `src` or just home directory.

    Notes
    -----
    * Writes config file to CWD / ".jaepeto.ini"
    """
    project = Path.cwd()
    config_path = project / ".jaepeto.ini"

    if config_path.exists():
        print(".jaepeto.ini already exists!")
        return

    config = ConfigParser()

    project_name = project.stem

    src_dir = project / "src"
    if src_dir.is_dir():
        srcdir = "src"
        for _file in src_dir.glob("*"):
            if _file.is_dir():
                package = _file.stem
                break
    else:
        srcdir = "."
        package = "."

    config.add_section("project")
    config.set("project", "name", project_name)
    config.set("project", "description", "<ENTER SHORT PROJECT DESCRIPTION>")
    config.set("project", "language", "python")
    config.set("project", "api_key", "<ADD API KEY HERE>")
    config.set("project", "srcdir", srcdir)
    config.set("project", "package", package)

    config.add_section("settings")
    config.set("settings", "num_class_uses_threshold", "3")
    config.set("settings", "max_num_entrypoints_threshold", "10")

    config.add_section("docs")
    config.set("docs", "docdir", "./")
    config.set("docs", "changelog", "CHANGELOG")

    print(f"Creating config file at {config_path}")
    with open(config_path, "w") as f:
        config.write(f)
