from pathlib import Path
from typing import Optional

import requests

from jaepeto.utils import post
from jaepeto.utils.parse_python import get_specific_python_function


def summarise_function(function_name: str, file: Path) -> Optional[str]:
    if function_str := get_specific_python_function(function_name, file):
        if summary_response := post("summarise", function_str.strip("\n")):
            if "summary" in summary_response:
                return summary_response["summary"]
