import ast
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union


def find_func_lines(node: Union[ast.FunctionDef, ast.ClassDef]):
    return node.lineno - 1, node.end_lineno - 1


def find_max_func_line(node: ast.FunctionDef):
    max_line = node.lineno

    if hasattr(node, "body"):
        for child in node.body:
            child_max = find_max_func_line(child)
            max_line = max(max_line, child_max)

    if isinstance(node, ast.If):
        for child in node.orelse:
            child_max = find_max_func_line(child)
            max_line = max(max_line, child_max)

    return max_line


def get_specific_python_function(function_name: str, file, max_length: int = 100):
    with open(file, "r") as source:
        tree = ast.parse(source.read())

    for node in tree.body:
        if not (isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef)):
            continue

        if node.name == function_name:
            func_start, func_end = find_func_lines(node)
            py_string = _read_python_func(file, func_start, func_end, max_length)

            # This is a hacky way to try to get working code. Not robust
            # TODO: improve and make robust
            try:
                ast.parse(py_string)
            except Exception:
                return _read_python_func(file, func_start, func_end + 1, max_length)
            else:
                return py_string


def get_func_lines(file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            yield find_func_lines(node)


def get_funcs_as_string(
    file, min_length: int = 6, max_length: int = 100, include_docstring: bool = False
):
    for (func_start, func_end) in get_func_lines(file):
        if 1 + func_end - func_start >= min_length:
            func_string = _read_python_func(file, func_start, func_end, max_length)

            if not include_docstring:
                func_string = _remove_docstring(func_string)

            yield func_string


def _remove_docstring(func_string):
    """
    Remove docstring from a function call.

    Notes
    -----
    * Naively searches for triple quotes
    """
    split_func = func_string.split('"""')

    # TODO: Will incorrectly parse code if triple quotes present in code body
    if len(split_func) >= 3:
        split_func[0] = (
            split_func[0].rstrip() + "\n"
        )  # rstrip also removes \n. TODO: use raw strings to avoid this
        split_func[2] = split_func[2].lstrip("\n")

        del split_func[1]

    return "".join(split_func)


def _read_python_func(
    file: Path, min_line: int, max_line: int, max_line_difference: int
) -> str:
    """
    Read a subset of lines in a Python function.

    Parameters
    ----------
    min_line : int
        The starting line number (inclusive) which to read
    max_line : int
        The end line number (inclusive) which to read
    file : pathlib.Path
        The file to read
    max_line_different : int
        Maximum amount of lines to read. Overrides `max_line`.

    Returns
    -------
    str
        Subset of lines from the given file
    """
    with open(file, "r") as source:
        code = source.readlines()

    max_line = min(max_line, min_line + max_line_difference - 1)

    return "".join(code[min_line : max_line + 1])


def identify_main_functions(file: Path):
    """
    Extract function names called in script's __main__ entrypoint.

    If script does not have `if __name__ == "__main__"`,
    then gracefully return an empty list.
    For each call, only detects than an object has been called;
    it does not check whether it's a method, a function, or something else.

    Parameters
    ----------
    file : pathlib.Path
        The path to the python file in which to search for the entrypoint

    Returns
    -------
    bool
        Whether the file has a __main__ entrypoint
    list of str
        The name of any object called with a __main__ entrypoint
    """
    with open(file, "r") as f:
        tree = ast.parse(f.read())

    called_funcs: List[str] = []
    has_main_entrypoint = False

    for _node in tree.body:
        if not isinstance(_node, ast.If):
            continue

        _node_test = _node.test

        if not isinstance(_node_test, ast.Compare):
            continue

        test_left = _node_test.left

        if not isinstance(test_left, ast.Name):
            # Might be a subscripted comparator, for example
            # Whatever it is, it's certainly not __name__
            continue

        if (
            test_left.id == "__name__"
            and isinstance(_node_test.ops[0], ast.Eq)
            and _node_test.comparators[0].value == "__main__"
        ):
            has_main_entrypoint = True

            for sub_node in _node.body:
                if isinstance(sub_node, ast.Expr) or isinstance(sub_node, ast.Assign):
                    sub_node_value = sub_node.value

                    if isinstance(sub_node_value, ast.Call):
                        called_funcs.extend(parse_ast_call(sub_node_value))

    return has_main_entrypoint, called_funcs


def parse_ast_call(node: ast.Call) -> List[str]:
    called_funcs: List[str] = []

    if _func_call := _parse_ast_func(node.func):
        called_funcs.append(_func_call)

    for _func_arg in node.args:
        if isinstance(_func_arg, ast.Call):
            called_funcs.extend(parse_ast_call(_func_arg))

    for _func_kwarg in node.keywords:
        if isinstance(_func_kwarg.value, ast.Call):
            called_funcs.extend(parse_ast_call(_func_kwarg.value))

    return called_funcs


def _parse_ast_func(node) -> Optional[str]:
    if isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Name):
        return node.id


def parse_all_type_hints(file: Path):
    """
    Extract type hints for each function/method in a given file.
    """
    with open(file, "r") as f:
        tree = ast.parse(f.read())

    function_hints = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            function_hints[node.name] = parse_function_type_hint(node)

    return function_hints


def parse_function_type_hint(code: ast.FunctionDef) -> List[str]:
    type_hints = []

    for arg in code.args.args:
        type_hints.extend(parse_type_hint(arg.annotation))

    return list(set(type_hints))


def parse_type_hint(annotation) -> List[str]:
    """
    Convert an ast annotation into a readable type.

    High-level types like "List" and "Tuple" are not resolved further,
    e.g. not to "list of list of str".
    Function can parse 3.10-style | operator.

    Parameters
    ----------
    annotation : ast object
        The ast annotation object to parse

    Returns
    -------
    list of str
        All high-level types conferred by the annotation
    """
    if isinstance(annotation, ast.Name):
        types = annotation.id.split("|")
        return [_type.strip() for _type in types]
    elif isinstance(annotation, ast.Attribute):
        return [parse_type_hint(annotation.value)[0] + "." + annotation.attr]
    elif isinstance(annotation, ast.Subscript):
        if annotation.value.id == "Union":
            types = []
            annotation_slice = annotation.slice

            # Slight API change between python 3.8 and 3.9
            if hasattr(annotation_slice, "elts"):
                # Python 3.9+ API
                for sub_type in annotation_slice.elts:
                    types.extend(parse_type_hint(sub_type))
            elif hasattr(annotation_slice, "value") and hasattr(
                annotation_slice.value, "elts"
            ):
                for sub_type in annotation_slice.value.elts:
                    types.extend(parse_type_hint(sub_type))

            return types
        elif annotation.value.id == "Optional":
            # TODO: get the subscripted type
            return []
        else:
            # Only care about list/tuple at high level atm.
            # Don't need to get exact type
            return [annotation.value.id.lower()]
    elif isinstance(annotation, ast.Constant):
        return [annotation.value]
    else:
        return []


def parse_argument_parser(file_contents):
    tree = ast.parse(file_contents)
    identifier = get_parser_identifier(tree)
    arguments = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Call)):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "add_argument"
                and func.value.id == identifier
            ):
                arg = node.args[0].value
                arguments.append(arg)
    return arguments


def get_parser_identifier(tree):
    for node in ast.walk(tree):

        if isinstance(node, (ast.Assign)):
            value = node.value
            if isinstance(value, (ast.Call)):
                call = value.func
                if isinstance(call, (ast.Attribute)) and call.attr == "ArgumentParser":
                    name = node.targets[0].id
                    return name
