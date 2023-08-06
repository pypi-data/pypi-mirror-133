"""
Write technical docs
"""
import os
import re
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple

from jaepeto.patterns import (
    CIParser,
    ContainerParser,
    describe_file_architecture,
    read_packages,
)
from jaepeto.structure import (
    DevOnboardingParser,
    FileAnalyser,
    OnboardingParser,
    get_script_entrypoints,
    group_imports_at_level,
    infer_important_functions,
)
from jaepeto.summaries import summarise_function
from jaepeto.utils import get_func_update, get_line_changes_for_file


def create_technical_doc(
    source_module_name: str,
    package_name: str,
    project_root: Path,
    technical_doc_file: Path,
    config,
    repo_info: str = None,
    project_title: str = "Project",
    project_summary: Optional[str] = None,
):
    if not technical_doc_file.exists():
        technical_doc_file.touch()

    with open(technical_doc_file, "r") as f:
        contents = f.readlines()

    contents = update_code_sections(contents)

    top_fixed_contents, bottom_fixed_contents = get_fixed_sections(contents)
    del contents

    # Add sections
    if top_fixed_contents == []:
        write_document_intro(technical_doc_file, project_title, project_summary)

    create_architecture_section(project_root, technical_doc_file)
    create_src_overview(
        source_module_name, package_name, project_root, technical_doc_file, config
    )
    create_developer_section(project_root, technical_doc_file)
    create_module_overview(source_module_name, project_root, technical_doc_file)

    # Re-add fixed sections
    with open(technical_doc_file, "r") as f:
        contents = f.readlines()

    contents = top_fixed_contents + contents + bottom_fixed_contents
    with open(technical_doc_file, "w") as f:
        f.writelines(contents)


def write_document_intro(technical_doc_file: Path, project_title: str, project_summary):
    with open(technical_doc_file, "w") as file:
        file.write(f"# {(project_title + ' Technical Documentation').strip()}")
        file.write(f"\n\n**Last updated:** {datetime.now().strftime('%Y-%m-%d')}\\")
        file.write("\n_Document generation aided by **Jaepeto**_")

        if project_summary:
            file.write(f"\n\n{project_summary}")

        file.write("\n\n* [Introduction](#introduction)")
        file.write("\n* [Code Overview](#code-overview)")

        file.write("\n\n## Introduction")
        file.write(
            f"""\n\nThis is a technical document detailing
        at a high-level
        what {project_title} does, how it operates,
        and how it is built.
        It is meant for consumption internally
        by technical developers
        and managers."""
        )

        file.write("\n\n### Scope")
        file.write(
            """\n\nThis document provides high-level summaries
        of the project codebase."""
        )

        file.write("\n\n### Context")
        file.write(
            """\n\nThe outline of this document was generated
        by **Jaepeto**.
        The documentation should be reviewed
        and detail provided manually
        before the documentation is released."""
        )


def create_architecture_section(project_root: Path, technical_doc_file: Path):
    arch_contents = ["\n\n## Project Architecture\n\n"]

    if packages := read_packages(project_root):
        arch_contents.append("The project has the following dependencies:\n")
        for _package in packages:
            arch_contents.append(f"\n* {_package}")
        arch_contents.append("\n\n")

    container_parser = ContainerParser()
    if container_description := container_parser.parse(project_root):
        container_arch = add_section_comments(
            "container", "arch", [container_description, "\n\n"]
        )
        arch_contents.extend(container_arch)

    arch_contents = add_section_comments("arch", "group", arch_contents)

    with open(technical_doc_file, "a") as file:
        file.writelines(arch_contents)


def create_developer_section(project_root: Path, technical_doc_file: Path) -> None:
    contents = ["\n\n## Developers"]

    # Requirements
    dev_onboarding = DevOnboardingParser()
    dev_onboarding.parse(project_root)

    if dev_setup := str(dev_onboarding):
        setup_info = add_section_comments("setup", "dev", [dev_setup, "\n\n"])
        contents.extend(setup_info)

    # CI
    ci_parser = CIParser()
    ci_parser.parse(project_root)

    if ci_description := str(ci_parser):
        ci_info = add_section_comments("ci", "dev", [ci_description, "\n\n"])
        contents.extend(ci_info)

    contents = add_section_comments("dev", "group", contents)

    with open(technical_doc_file, "a") as file:
        file.writelines(contents)


def create_src_overview(
    module_name: str,
    package_name: str,
    project_root: Path,
    technical_doc_file: Path,
    config,
) -> None:
    """
    Write high-level overview of project to technical doc.

    Minimum version.
    Entrypoints and entrypoint summaries.
    CI/CD processes used.
    Dockerfiles.
    Writes this information to technical document in project.

    Parameters
    ----------
    module_name : str
        The path from project root to the source code. In a project with a src directory, this would be `src/myproj`.
    package_name : str
        The name of the project package as it would get installed.
        In a project with a src directory `src/myproj`, this would probably be `myproj`.
    project_root : pathlib.Path
        Full path to project root
    technical_doc_file : pathlib.Path
        Path to technical document in project
    config : dict
        A fully-parsed config dict
    """
    source_code_dir = project_root / module_name
    contents = ["\n\n## Code Overview\n\n"]

    # Describe setup
    setup_parser = OnboardingParser()
    setup_parser.parse(source_code_dir, project_root, package_name)

    if setup_description := str(setup_parser):
        setup_contents = add_section_comments(
            "setup", "helloworld", [setup_description, "\n\n"]
        )
        contents.extend(setup_contents)
        del setup_contents

    # Important / __main__/__init__ functions
    entrypoint_contents = ["\n\n## Entrypoints\n\n"]
    entrypoints = infer_important_functions(package_name, source_code_dir)
    num_entrypoints = len(entrypoints)

    if 0 < num_entrypoints <= config["settings"]["max_num_entrypoints_threshold"]:
        entrypoint_contents.append(
            f"There are {num_entrypoints} source code objects in top-level `__main__`/`__init__`:\n\n"
        )
        for _entrypoint in entrypoints:
            entrypoint_func = _entrypoint.split(".")[-1]
            entrypoint_file = (os.sep).join(_entrypoint.split(".")[:-1]) + ".py"
            entrypoint_contents.append(
                f"### `{entrypoint_func}` from `{entrypoint_file}`\n"
            )

            _entrypoint_doc = summarise_function(
                entrypoint_func, project_root / entrypoint_file
            )
            if _entrypoint_doc:
                entrypoint_contents.append(f" \n```python\n{_entrypoint_doc}\n```\n")
            else:
                entrypoint_contents.append("\nObject cannot be summarised.\n")

        entrypoint_contents.append(
            "\nThese entrypoints are broken down into the following modules:\n\n"
        )
    elif num_entrypoints == 0:
        entrypoint_contents.append(
            f"There are 0 source code entrypoints in top-level `__main__`/`__init__` files.\n"
        )
    else:
        entrypoint_contents.append(
            f"""There are {num_entrypoints} source code objects
                        in top-level `__main__`/`__init__`.
                        They are broken down into the following modules:\n\n"""
        )

    entrypoint_groups = group_imports_at_level(entrypoints, level=2)

    for _entrypoint, _count in entrypoint_groups:
        entrypoint_contents.append(f"* `{_entrypoint}` has {_count} entrypoints\n")

    entrypoint_contents.append("\n")

    # Scripts with __name__ == __main__ and function calls
    script_entrypoints = get_script_entrypoints(source_code_dir, project_root)
    for _file, _entrypoints in script_entrypoints.items():
        if not _entrypoints:
            contents.append(f"`{_file}`` has a `__main__` entrypoint.\n\n")
        else:
            contents.append(f"`{_file}` has a `__main__` entrypoint, which calls:\n\n")
            for _entrypoint in _entrypoints:
                contents.append(f"* `{_entrypoint}`\n")
            contents.append("\n")

    contents.extend(
        add_section_comments("entrypoints", "helloworld", entrypoint_contents)
    )
    del entrypoint_contents

    # Classes used around the codebase
    class_type_hints = FileAnalyser(package_name, source_code_dir).parse()
    important_classes = []
    class_contents = []

    for class_name, class_uses in class_type_hints.items():
        if len(class_uses[1]) >= config["settings"]["num_class_uses_threshold"]:
            important_classes.append(
                f"`{class_name}` is a base class. It is used {len(class_uses[1])} times."
            ) if class_uses[0] is None else important_classes.append(
                f"`{class_name} inherits from {', '.join(class_uses[1])}"
            )

    if important_classes:
        class_contents.append(
            "The project has classes which are used in multiple functions:\n\n"
        )
        for _important_class in important_classes:
            class_contents.append(f"* {_important_class}\n")
        class_contents.append("\n")

        contents.extend(add_section_comments("classes", "helloworld", class_contents))
        del class_contents

    contents = add_section_comments("helloworld", "group", contents)

    with open(technical_doc_file, "a") as file:
        file.writelines(contents)


def create_module_overview(
    module_name: str, project_root: Path, technical_doc_file: Path
):
    """
    Create an overview of Python file structure in the project.
    """
    doc_contents, _ = _create_module_overview(
        project_root / module_name,
        project_root,
        [f"\n### **{project_root.stem}/**"],
        0,
    )

    if len(doc_contents) > 1:
        # if == 1, then only header was present but no python files. Therefore exclude.
        with open(technical_doc_file, "a") as file:
            file.writelines(doc_contents)


def _create_module_overview(module_path: Path, root: Path, doc_contents, n_calls: int):
    """
    Create an overview of Python file structure in the project.

    Include directories and subdirectories if they contain at least 1 python file.
    For each file, describe the rate of the change of the file,
    an inferred owner, and consequences of the file such as API or database calls.

    Parameters
    ----------
    module_path : pathlib.Path
        The path to the current directory being explored
    root : pathlib.Path
        The path to the top-level project directory.
        Used to infer local path to file (from top-level dir).
    doc_contents : list of str
        List containing contents above in the directory structure
        to be added to documentation
    n_calls : int
        DEPRECATED. Number of calls to API in this module overview section

    Returns
    -------
    list or str
        The contents to add to the documentation
    int
        DEPRECATED. The total number of API calls in this section
    """
    hash_level = min(6, len(doc_contents[-1].replace("\n", "").split()[0]) + 1)

    for subdir in module_path.glob("*"):
        if subdir.stem == "__pycache__":
            continue

        if subdir.is_dir():
            new_doc_contents, n_calls = _create_module_overview(
                subdir, root, [f"\n\n{'#' * hash_level} {subdir.stem}/"], n_calls
            )
            if len(new_doc_contents) > 1:
                doc_contents.extend(new_doc_contents)

    for py_file in module_path.glob("*.py"):
        if py_file.stem == "__init__":
            continue

        relative_file_path = str(py_file.relative_to(root))
        lines_added, lines_removed, most_common_author = get_line_changes_for_file(
            relative_file_path
        )

        if (lines_added + lines_removed) >= 20:
            doc_contents.append("\n\n")
            doc_contents.append(f"<!---Jaepeto-section-file: {relative_file_path}--->")
            doc_contents.append(f"\n\n{'#' * hash_level} {py_file.stem}.py")

            file_summary_str = dedent(
                f"""
                \n\nFile has {lines_added} lines added and {lines_removed} lines removed
                in the past 4 weeks."""
            )

            if most_common_author:
                file_summary_str += f" {most_common_author} is the inferred code owner."

            doc_contents.append(file_summary_str + "\n")

        if file_arch := describe_file_architecture(py_file):
            doc_contents.append(file_arch)

    return doc_contents, n_calls


def get_fixed_sections(doc_contents: List[str]) -> Tuple[List[str], List[str]]:
    """
    Get all of the top-fixed and bottom-fixed doc sections from the doc.

    Sections can be fixed to "top" or "bottom".
    Top-fixed sections have new content appended below them.
    Bottom-fixed sections have new content appended above them.

    Parameters
    ----------
    doc_contents : list of str
        The document

    Returns
    -------
    list of str
        Section contents which have been fixed to the top of the doc
    list of str
        Section contents which have been fixed to the bottom of the doc
    """
    return _get_fixed_section("top", doc_contents), _get_fixed_section(
        "bottom", doc_contents
    )


def _get_fixed_section(position: str, doc_contents: List[str]) -> List[str]:
    section = []
    section_count = 1

    while True:
        if section_content := get_doc_section(
            f"{position}{section_count}-start",
            f"{position}{section_count}-end",
            "fixed",
            doc_contents,
        ):
            section.extend(section_content)
            section_count += 1
        else:
            break

    return section


def has_section(name: str, section_type: str, doc_contents: List[str]) -> bool:
    comment = f"<!---Jaepeto-section-{section_type}: {name}-" + "{}--->\n"
    return (
        comment.format("start") in doc_contents
        and comment.format("end") in doc_contents
    )


def update_doc_code_sections(doc_file: Path) -> None:
    with open(doc_file, "r") as f:
        contents = f.readlines()

    contents = update_code_sections(contents)

    with open(doc_file, "w") as f:
        f.writelines(contents)


def update_code_sections(doc_contents: List[str]) -> List[str]:
    """
    Update every code section in a document to the latest API.

    Code sections are marked by a Jaepeto-section-code comment.
    Code sections do not need an -end comment.
    Code sections are terminated by open-closed ``` (code indicators).
    If another section starts before a code section is opened or closed,
    the block is not recognised as a code section.

    Parameters
    ----------
    doc_contents : list of str
        The document contents in which to search for code

    Returns
    -------
    list of str
        Document contents with code sections updated for latest commit.
    """
    new_code_blocks = []

    for idx, line in enumerate(doc_contents):
        if line.startswith("<!---Jaepeto-section-code:"):
            if new_code_info := update_code_section(idx, doc_contents):
                new_code_blocks.append(new_code_info)

    updated_doc_contents = doc_contents.copy()
    for start_idx, end_idx, new_code in new_code_blocks:
        updated_doc_contents = (
            updated_doc_contents[:start_idx]
            + [new_code]
            + updated_doc_contents[end_idx + 1 :]
        )

    return updated_doc_contents


def update_code_section(
    start_idx: int, doc_contents: List[str]
) -> Optional[Tuple[int, int, List[str]]]:
    """
    Identify and update a code snippet based on latest revision.

    To be updated, the comment attached to a code snippet
    must have the name of form {hash-start}-{file}-{line-start}-{line-end}.
    If opening or closing ``` are not detected, the code section is not updated.

    Parameters
    ----------
    start_idx : int
        The index of the beginning of a suspected code block to be updated
        within `doc_contents`
    doc_contents : list of str
        Documentation containing code blocks

    Returns
    -------
    None or (int, int, list of str)
        int = The start index of the OLD code block
        int = The end index of the OLD code block
        list of str = The NEW code block (inc. comment)
        Return None if code block not detected OR did not update.
    """
    comment = doc_contents[start_idx]
    if code_info_match := re.search(
        r" ([a-zA-Z0-9]{5,8})-(.+)-([0-9]{1,5})-([0-9]{1,5})", comment
    ):
        commit = code_info_match.group(1)
        code_file = code_info_match.group(2)
        code_start_line = int(code_info_match.group(3))
        code_end_line = int(code_info_match.group(4))

    object_name = None
    object_is_class = None
    code_started = False

    for idx, doc_line in enumerate(doc_contents[start_idx + 1 :]):
        doc_line = doc_line.strip()

        if doc_line.startswith("```"):
            if code_started and object_name:
                # Have reached the end of the code block
                # and have detected a trackable code object
                try:
                    if new_func_update := get_func_update(
                        code_file, object_name, commit
                    ):
                        latest_commit, _, new_file, new_code = new_func_update

                        new_code_selected_line = "\n".join(
                            new_code.split("\n")[: code_end_line - code_start_line + 1]
                        )
                        new_code_str = dedent(
                            f"""
<!---Jaepeto-section-code: {latest_commit}-{new_file}-{code_start_line}-{code_end_line}--->
```python
{new_code_selected_line}
```
"""
                        )
                        return start_idx, idx, new_code_str
                    else:
                        return None
                except:
                    return None
            else:
                code_started = True
        elif func_match := re.match(r"def (\w+)\(", doc_line):
            object_name = func_match.group(1)
            object_is_class = False
        elif class_match := re.match(r"class (\w+)[:\(]", doc_line):
            object_name = class_match.group(1)
            object_is_class = True

    return None


# --- Doc section management
def add_section_comments(
    section_name: str, section_type: str, contents: List[str]
) -> List[str]:
    """
    Bookend documentation contents with section-marking markdown comments.

    Prepends a `section-name`-start comment
    and append a `section-name`-end comment.
    """
    comment_base = f"<!---Jaepeto-section-{section_type}: {section_name}-" + "{}--->"
    return (
        ["\n", comment_base.format("start"), "\n"]
        + contents
        + ["\n", comment_base.format("end"), "\n"]
    )


def append_to_section(
    new_content: str, all_content: List[str], section_name: str, section_type: str
) -> List[str]:
    """
    Add documentation to a Jaepeto auto-generated section.

    Sections are detected by "Jaepeto-section" markdown comments.
    If a section comment with name "section_name"-end does not exist,
    the section is assumed to have ended when the next "Jaepeto-section"
    comment appears in the file.
    If the comment section is not in the file contents,
    returns file contents without the new contents added.

    Parameters
    ----------
    new_content : str
        The content to add to the documentation
    all_content : list of str
        The current documentation contents
    section_name : str
        The section name in the markdown comment to look for, in which to place the new content
    section_type : str
        The type of section to look out for. Should be "file"

    Returns
    -------
    list of str
        `all_content` with `new_content` added to the given section, if it exists
    """
    updated_content = all_content.copy()

    if not new_content.endswith("\n"):
        new_content += "\n"

    try:
        section_index_end = updated_content.index(
            f"<!---Jaepeto-section-{section_type}: {section_name}-end--->\n"
        )
        updated_content.insert(section_index_end, new_content)
        updated_content.insert(section_index_end + 1, "\n")
        return updated_content
    except ValueError:
        try:
            section_index = updated_content.index(
                f"<!---Jaepeto-section-{section_type}: {section_name}--->\n"
            )
        except ValueError:
            return updated_content
        else:
            for index in range(section_index + 1, len(updated_content)):
                if updated_content[index].startswith("<!---Jaepeto-section"):
                    updated_content.insert(index, new_content)
                    return updated_content

            # If got to here, no new section start, so just put new content at the end
            updated_content.append(new_content)
            return updated_content


def get_doc_section(
    section_start_name: str,
    section_end_name: str,
    section_type: str,
    doc_contents: List[str],
) -> List[str]:
    try:
        section_start_index = doc_contents.index(
            f"<!---Jaepeto-section-{section_type}: {section_start_name}--->\n"
        )
        section_end_index = doc_contents.index(
            f"<!---Jaepeto-section-{section_type}: {section_end_name}--->\n"
        )
    except ValueError:
        return []
    else:
        return doc_contents[section_start_index : section_end_index + 1]


def replace_doc_section(
    section_start_name: str,
    section_end_name: str,
    section_type: str,
    new_contents: List[str],
    doc_contents: List[str],
) -> List[str]:
    try:
        section_start_index = doc_contents.index(
            f"<!---Jaepeto-section-{section_type}: {section_start_name}--->\n"
        )
        section_end_index = doc_contents.index(
            f"<!---Jaepeto-section-{section_type}: {section_end_name}--->\n"
        )
    except ValueError:
        return doc_contents
    else:
        new_doc_contents = doc_contents.copy()
        new_doc_contents[section_start_index : section_end_index + 1] = new_contents
        return new_doc_contents
