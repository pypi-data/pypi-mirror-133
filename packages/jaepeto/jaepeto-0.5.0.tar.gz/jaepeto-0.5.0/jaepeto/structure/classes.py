"""
Identify and analyse how classes are used in the project.
"""
import ast
import os
from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional, Tuple

from jaepeto.structure.entrypoint import identify_module_imports, resolve_import_paths
from jaepeto.utils import parse_all_type_hints


class FileAnalyser:
    def __init__(self, module_name: str, module_root: Path, max_depth: int = 3):
        self.__module_name = module_name
        self.__module_root = module_root
        self.__max_depth = max_depth

    def fetch_class_names(self, file_contents: str) -> List[str]:
        """
        Fetch all class names present in a file.

        If no class names are present, return an empty list.

        Parameters
        ----------
        file_contents : str
            Contents of a file as a single string

        Returns
        -------
        list of str
            List of all class names defined in the file
        """
        tree = ast.parse(file_contents)
        names: List[str] = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                names.append(node.name)

        return names

    def get_class_names(self) -> List[Tuple[str, str]]:
        """
        Fetch the names of all custom classes created in a project.

        Returns
        -------
        list of (str, str) tuples
            First element of tuple is the class name
            Second element of tuple is the "." separated import path to the class name, excluding the class
                e.g. ("MyClass", "root.subdir.subsubdir.file")
        """
        class_names: List[str] = []

        for py_file in self.__module_root.rglob("*.py"):
            file_prefix = ".".join(
                str(py_file.relative_to(self.__module_root).with_suffix("")).split(
                    os.sep
                )
            )

            if len(file_prefix.split(".")) > self.__max_depth:
                continue

            with open(py_file, "r") as f:
                names = self.fetch_class_names(f.read())

            class_names.extend([(name, file_prefix) for name in names])
        return class_names

    def get_base_classes(self, class_path: str) -> Optional[List[str]]:
        """
        Fetch the names of all base classes inherited by a class.

        Parameters
        ----------
        class_path : str
            Path of class seperated by ".". eg root.subdir.subsubdir.file
        src_path: Path
            root path of project

        Returns
        -------
        None if there are no base classes inheritted by the class
        List of Base names as strings
        """
        class_name = class_path.split(".")[-1]
        class_absolute_path = self.__module_root / (
            os.sep.join(class_path.split(".")[1:-1]) + ".py"
        )
        with open(str(class_absolute_path), "r") as f:
            data = f.read()
            for node in ast.parse(data).body:
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    return (
                        None
                        if len(node.bases) == 0
                        else [parent.id for parent in node.bases]
                    )
            return None

    def parse(self) -> Dict[str, Optional[List[str]]]:
        """
        Fetch the names of all base classes inherited by a class.

        Returns
        -------
        Dictionary of important class as strings and the respective List of  string Base names
        as values
        """
        class_mapping: Dict = {}
        important_classes = self.resolve_class_uses()
        for important_class in important_classes:
            bases = self.get_base_classes(important_class)
            class_mapping[important_class] = (bases, important_classes[important_class])
        return class_mapping

    def resolve_class_uses(self) -> DefaultDict[str, list]:
        """
        Find every occurrence where a class is used as a type hint.

        Returns
        -------
        dict of str: list of str
            Keys are import paths to a class, e.g. `module.sub.file.ClassName`
            Values are list of path to every function where class is used as a type hint
        """

        class_uses = defaultdict(list)

        for py_file in self.__module_root.rglob("*.py"):
            local_path = ".".join(
                str(py_file.relative_to(self.__module_root).with_suffix("")).split(
                    os.sep
                )
            )
            if len(local_path.split(".")) > self.__max_depth:
                continue

            local_path = self.__module_name + "." + local_path
            local_module = ".".join(local_path.split(".")[:-1])  # exclude file

            with open(py_file, "r") as f:
                contents = f.read()

            imports = identify_module_imports(local_module, contents.split("\n"))
            type_hints = parse_all_type_hints(py_file)
            local_classes = self.fetch_class_names(contents)
            for func, types in type_hints.items():
                for import_path, import_statement in imports:
                    if import_statement in types:
                        class_uses[import_path].append((local_path + "." + func))

                for _type in types:
                    if _type in local_classes:
                        class_uses[local_path + "." + _type].append(
                            local_path + "." + func
                        )

        return class_uses
