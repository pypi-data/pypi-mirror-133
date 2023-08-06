"""
Making requests to server
"""
import hashlib
import json
import os
from typing import List, Union

import requests

SERVER_DOMAIN = "https://x0jfh97rfl.execute-api.eu-west-2.amazonaws.com/Prod/"


def post(endpoint: str, payload: Union[str, List[str]]) -> Union[None, str, List[str]]:
    proj_name = os.getenv("JAEPETO_PROJECT_NAME", "DefaultProject")

    hashed_project = hashlib.sha224(proj_name.encode("utf-8")).hexdigest()

    api_key = os.getenv("JAEPETO_API_KEY")
    run_locally = os.getenv("JAEPETO_RUN_LOCALLY", "False") == "True"

    if not (api_key or run_locally):
        return None

    server_domain = SERVER_DOMAIN if not run_locally else "http://127.0.0.1:3000/"

    try:
        response = requests.post(
            server_domain + endpoint + f"?project={hashed_project}",
            data=json.dumps(payload),
            headers={
                "x-api-key": api_key
                or "DummyKey",  # dummy key if not present and running locally
                "content-type": "application/json",
            },
        )
    except requests.exceptions.ConnectionError:
        # Happens if running locally but server hasn't set up (or API server has crashed!)
        return None

    if response.status_code == 200:
        message = response.json()["message"]
        if isinstance(message, list):
            return message

        try:
            message = json.loads(message)
        except Exception:
            pass
        return message
    else:
        return None
