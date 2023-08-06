"""
Third-party tools
e.g., Coverage, Docker
"""
import os
import re
from pathlib import Path
from typing import List, Optional, Tuple

import requests

from jaepeto.utils import post


class ContainerParser:
    def __init__(self) -> None:
        self.file: Optional[str] = None

    def parse(self, project_dir: Path) -> Optional[str]:
        for spelling in ("dockerfile", "Dockerfile", "DOCKERFILE"):
            if spelling not in os.listdir(project_dir):
                continue

            self.file = spelling

            with open(project_dir / spelling, "r") as file:
                docker_contents = file.readlines()

            return post("parse-container", docker_contents)
        return None


class CIParser:
    def __init__(self) -> None:
        self.ci_names: List[str] = []
        self.ci_summaries: List[Tuple[str, str]] = []

    def parse(self, project_dir: Path) -> None:
        """
        Look through project for presence of CI files.

        Detects CI files and parses the files
        to infer some information about what the script is doing.
        """
        ci_files = {
            "Travis": [".travis.yml", "travis.yml", ".travis.yaml", "travis.yaml"],
            "GitHub Actions": [f".github{os.sep}workflows"],
            "Circle CI": [f".circleci{os.sep}config.yml"],
            "GitLab CI": [".gitlab-ci.yml"],
        }

        for ci_provider, file_names in ci_files.items():
            for file_name in file_names:
                if (project_dir / file_name).exists():
                    self.ci_names.append(ci_provider)
                    self.parse_ci_files(ci_provider, project_dir / file_name)
                    break

    def parse_ci_files(self, ci_provider: str, file_path: Path) -> None:
        """
        Parse a CI file for useful information.

        Information includes when the scripts are executed
        and what they do (i.e. what type of testing, or to where something is deployed).
        If a CI file is parsed, information is added to an attribute of this class.
        Only parses GitHub actions currently.

        Parameters
        ----------
        ci_provider : str
            The name of the CI provider detected (e.g. "GitLab CI")
        file_path : pathlib.Path
            Path to the file detected which signals presence of CI
        """
        if ci_provider == "GitHub Actions":
            for github_action in file_path.glob("*.yml"):
                github_action_name = github_action.stem

                with open(github_action, "r") as f:
                    contents = f.read()

                ci_summary = post("parse-ci/github", contents)
                self.ci_summaries.append((github_action_name, ci_summary))

    def __str__(self) -> str:
        if self.ci_names:
            if len(self.ci_names) == 1:
                arch = f"The project uses {self.ci_names[0]} for CI/CD."
            else:
                arch = f"The project uses multiple CI/CD providers: {', '.join(self.ci_names)}"

            # Table of CI file purposes, if present
            if self.ci_summaries:
                arch += "\n\n| CI File | Purpose |\n|:----|:----|"

            for ci_file, ci_summary in self.ci_summaries:
                arch += f"\n| {ci_file} | {ci_summary if ci_summary else ''} |"
        else:
            arch = "No CI/CD config files were detected."

        return arch
