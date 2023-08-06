from argparse import ArgumentParser
from pathlib import Path

from jaepeto.docs.changelog import ChangelogDoc
from jaepeto.docs.technical_docs import (
    append_to_section,
    create_technical_doc,
    update_doc_code_sections,
)
from jaepeto.utils import parse_config, post


def generate_documentation() -> None:
    """
    Generate and save documentation.

    This is a CLI entrypoint to the codebase.
    The current working directory must be the root of the project
    for which documentation is to be generated.
    The root project must contain a `.jaepeto.ini` file.
    """
    parser = ArgumentParser("CLI entrypoint for documentation generation")
    parser.add_argument("document", nargs="?", default="technical")
    parser.set_defaults(changelog=False)
    args = parser.parse_args()

    config_path = Path.cwd()
    config = parse_config(config_path)
    arg = args.document.lower()

    if arg == "changelog":
        changelog_path = config_path / config["docs"]["changelog"]
        changelog = ChangelogDoc(changelog_path)
        changelog.generate()
        changelog.save()

        post("notify", None)
        print(f"Successfully generated CHANGELOG at {changelog_path}")
    elif arg == "code":
        tech_doc_path = (
            config_path / config["doc_dir"] / config["docs"]["technical_name"]
        ).with_suffix(".md")

        post("notify", None)

        update_doc_code_sections(tech_doc_path)
        print(f"Updated code snippets in {tech_doc_path}")
    else:
        tech_doc_path = (
            config_path / config["doc_dir"] / config["docs"]["technical_name"]
        ).with_suffix(".md")

        post("notify", None)

        create_technical_doc(
            config["src"],
            config["package"],
            config_path,
            tech_doc_path,
            config,
            project_title=config["name"],
            project_summary=config["description"],
        )
        print(f"Successfully generated technical documentation at {tech_doc_path}")
