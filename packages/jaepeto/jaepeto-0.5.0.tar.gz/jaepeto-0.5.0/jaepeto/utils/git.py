import re
import subprocess
from collections import defaultdict
from datetime import datetime
from typing import Optional, Tuple

from jaepeto.utils.parse_python import get_specific_python_function

leading_4_spaces = re.compile("^    ")


def get_commits(since_date: Optional[str] = None, until_date: Optional[str] = None):
    if since_date and until_date:
        command = ["git", "log", "--stat", "--since", since_date, "--until", until_date]
    else:
        command = ["git", "log", "--stat"]

    lines = (
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        .decode("utf-8")
        .split("\n")
    )

    commits = []
    current_commit = {}

    def save_current_commit():
        title = current_commit["message"][0]
        message = current_commit["message"][1:]
        changed_files = []

        if message and message[0] == "":
            del message[0]

        current_commit["title"] = title
        current_commit["message"] = "\n".join(message)
        current_commit["files"] = [
            _m.split("|")[0].strip() for _m in message if "|" in _m
        ]
        commits.append(current_commit)

    for line in lines:
        if not line.startswith(" "):
            if line.startswith("commit "):
                if current_commit:
                    save_current_commit()
                    current_commit = {}
                current_commit["hash"] = line.split("commit ")[1]
            else:
                try:
                    key, value = line.split(":", 1)
                    current_commit[key.lower()] = value.strip()
                except ValueError:
                    pass
        else:
            current_commit.setdefault("message", []).append(
                leading_4_spaces.sub("", line)
            )

    if current_commit:
        save_current_commit()

    commits.reverse()  # earliest commit first
    return commits


def find_earliest_commit_with_file(file: str, commits):
    # Assume commits are ordered earliest to latest
    for commit in commits:
        for commit_file in commit["files"]:
            if file in commit_file.lower():
                # Accepts partial match e.g. .travis -> .travis.yml
                return convert_datetime_to_date_string(commit["date"])

    raise RuntimeError(f"No commits involve file {file}")


def get_diff_for_file(file: str, commits):
    changes = []

    for i in range(1, len(commits)):
        main_commit = commits[i]

        if file not in main_commit["files"]:
            continue

        previous_commit_hash = commits[i - 1]["hash"]
        main_commit_hash = main_commit["hash"]

        lines = (
            subprocess.check_output(
                ["git", "diff", previous_commit_hash, main_commit_hash, file],
                stderr=subprocess.STDOUT,
            )
            .decode("utf-8")
            .split("\n")
        )

        lines = [l for l in lines if re.match("[+-][a-zA-Z]", l)]

        formatted_date = convert_datetime_to_date_string(main_commit["date"])
        changes.append((main_commit_hash, formatted_date, lines))

    return changes


def convert_datetime_to_date_string(datetime_string):
    return datetime.strptime(datetime_string, "%a %b %d %H:%M:%S %Y %z").strftime(
        "%Y-%m-%d"
    )


def get_line_changes_for_file(file: str):
    lines = (
        subprocess.check_output(
            ["git", "log", "-p", '--since="4 weeks ago"', "--", file],
            stderr=subprocess.STDOUT,
        )
        .decode("utf-8")
        .split("\n")
    )

    commits = []
    current_commit = {}

    def _save_current_commit():
        title = current_commit["message"][0]
        message = current_commit["message"][1:]
        changed_files = []

        if message and message[0] == "":
            del message[0]

        current_commit["title"] = title
        commit_message = "\n".join(message)

        if "additions" in current_commit:
            lines_added = len(current_commit["additions"])
        else:
            lines_added = 0

        if "deletions" in current_commit:
            lines_removed = len(current_commit["deletions"])
        else:
            lines_removed = 0

        commits.append((lines_added, lines_removed, current_commit["author"]))

    for line in lines:
        if not line.startswith(" "):
            if line.startswith("commit "):
                if current_commit:
                    _save_current_commit()
                    current_commit = {}
                current_commit["hash"] = line.split("commit ")[1]
            else:
                if line == "+" or re.match(r"\+[^\+]", line):
                    current_commit.setdefault("additions", []).append(line)
                elif line == "-" or re.match(r"-[^-]", line):
                    current_commit.setdefault("deletions", []).append(line)
                else:
                    try:
                        key, value = line.split(":", 1)
                        current_commit[key.lower()] = value.strip()
                    except ValueError:
                        pass
        else:
            current_commit.setdefault("message", []).append(
                leading_4_spaces.sub("", line)
            )

    if current_commit:
        _save_current_commit()

    authors = {}
    for _added, _removed, _author in commits:
        authors.setdefault(_author, 0)
        authors[_author] += _added + _removed

    if authors:
        common_author = max(authors, key=authors.get)
    else:
        common_author = None

    return sum([c[0] for c in commits]), sum([c[1] for c in commits]), common_author


def _get_tag_date(tag_name: str) -> str:
    return (
        subprocess.check_output(
            ["git", "log", "-1", "--format=%ai", tag_name], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split(" ")[0]
    )


def list_tags():
    tags = (
        subprocess.check_output(["git", "tag", "-n"], stderr=subprocess.STDOUT)
        .decode("utf-8")
        .split("\n")
    )
    tags.reverse()

    tags = [t.split(" ")[0] for t in tags]
    tags = [(t, _get_tag_date(t)) for t in tags if t]
    return tags


def get_func_update(
    filepath: str, object_name: str, commit: str, is_class: bool = False
) -> Optional[Tuple[str, str, str]]:
    """Track the evolution of a function/class/method from a given commit.

    Parameters
    ----------
    filepath : str
        The file in which the object is present

    Returns
    -------
    (str, str, str, str) or None
        The latest commit with the object
        The latest name of the object
        The latest file in which the object presides
        The latest code for the object
        or None if object cannot be tracked.
    """
    last_change = (
        subprocess.check_output(
            [
                "git",
                "blame",
                filepath,
                "-L",
                ":" + object_name,
                "--reverse",
                commit,
            ],
            stderr=subprocess.STDOUT,
        )
        .decode("utf-8")
        .split("\n")
    )[0]

    last_commit_change = last_change.split(" ")[0].strip()
    last_file_change = last_change.split(" ")[1].strip()

    if last_file_change.startswith("("):
        last_file_change = filepath

    if not _get_next_commit(last_commit_change):
        # Is most recent commit, therefore cannot be other changes
        return (
            last_commit_change.lstrip("^"),
            object_name,
            last_file_change,
            get_specific_python_function(object_name, last_file_change),
        )

    """if new_file_info := _find_new_object_file(
        object_name, last_commit_change, is_class=is_class
    ):  # has func moved files?
        new_object_file, new_commit = new_file_info
        return get_func_update(
            new_object_file, object_name, new_commit, is_class=is_class
        )"""
    if new_object_info := _find_new_object_name(
        object_name, last_commit_change, is_class=is_class
    ):  # has func changed name?
        new_object_name, new_commit = new_object_info
        return get_func_update(filepath, new_object_name, new_commit, is_class=is_class)
    else:
        return


def _find_new_object_file(
    object_name, commit: str, is_class: bool
) -> Optional[Tuple[str, str]]:
    obj_def = "def" if not is_class else "class"

    if next_commit := _get_next_commit(commit):
        git_diff = subprocess.check_output(
            ["git", "diff", commit, next_commit], stderr=subprocess.STDOUT
        ).decode("utf-8")

        if not (
            f"-{obj_def} {object_name}(" in git_diff
            and f"+{obj_def} {object_name}(" in git_diff
        ):
            return

        if new_file_match := re.search(
            rf"\+\+\+ b/([^\s]*)\n.*?\n.*?\+{obj_def} {object_name}\(", git_diff
        ):
            return new_file_match.group(1), next_commit


def _find_new_object_name(
    object_name: str, commit: str, is_class: bool
) -> Optional[Tuple[str, str]]:
    obj_def = "def" if not is_class else "class"

    if next_commit := _get_next_commit(commit):
        git_diff = (
            subprocess.check_output(
                ["git", "diff", commit, next_commit], stderr=subprocess.STDOUT
            )
            .decode("utf-8")
            .split("\n")
        )

        for idx, diff in enumerate(git_diff):
            if (
                diff.startswith(f"-{obj_def} {object_name}(")
                and idx < len(git_diff) - 1
            ):
                new_obj = git_diff[idx + 1]

                if new_obj.startswith(f"+{obj_def} "):
                    new_obj_name = (
                        git_diff[idx + 1].lstrip(f"+{obj_def}").split("(")[0].strip()
                    )
                    return new_obj_name, next_commit


def _get_next_commit(commit: str) -> Optional[str]:
    commit = commit.lstrip("^")

    if commit == get_current_commit():
        return None

    commit_tree = (
        subprocess.check_output(
            ["git", "log", "--reverse", "--ancestry-path", f"{commit}^..HEAD"],
            stderr=subprocess.STDOUT,
        )
        .decode("utf-8")
        .split("\nAuthor")
    )[
        1
    ]  # 0th entry is `commit`, 1st entry is the commit after `commit`

    next_commits = commit_tree.split("commit ")

    if len(next_commits) == 1:
        return None
    else:
        return next_commits[-1].strip()[:7]


def get_current_commit() -> Optional[str]:
    """
    Get the shortform of the current git commit, if using git.

    Returns
    -------
    str
        Shortform (first 7 digits) of the latest git commit, if git is used and there are commits.
        Otherwise, return None.
    """
    try:
        output = subprocess.check_output(["git", "log", "-1", "--oneline"]).decode(
            "utf-8"
        )
        return output.split(" ")[0]
    except subprocess.CalledProcessError:
        return None
