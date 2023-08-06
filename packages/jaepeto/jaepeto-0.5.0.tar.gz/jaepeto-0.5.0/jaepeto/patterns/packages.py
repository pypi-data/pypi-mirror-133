"""
Detect important environmental packages/libraries.
"""
import os
import re
from pathlib import Path
from typing import List

from jaepeto.utils import post


def read_packages(project_dir: Path) -> List[str]:
    packages = []

    if "requirements.txt" in os.listdir(project_dir):
        with open(project_dir / "requirements.txt", "r") as f:
            contents = f.readlines()

        if new_packages := post("parse-reqs/requirements", contents):
            packages.extend(new_packages)

    for _file in ("environment.yml", "environment.yaml"):
        if _file in os.listdir(project_dir):
            with open(project_dir / _file, "r") as f:
                contents = f.readlines()

            if new_packages := post("parse-reqs/environment", contents):
                packages.extend(new_packages)

    return packages
