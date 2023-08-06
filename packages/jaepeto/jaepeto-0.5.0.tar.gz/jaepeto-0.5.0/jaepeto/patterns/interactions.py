from pathlib import Path

from jaepeto.utils import post


def detect_requests_calls(file_contents: str) -> bool:
    available_request_methods = [
        method
        for method in ["get", "post", "put", "patch", "delete"]
        if f"requests.{method}(" in file_contents
    ]
    return len(available_request_methods) > 0


def detect_boto3_calls(file_contents: str) -> bool:
    return "boto3.resource" in file_contents


def detect_mongodb_calls(file_contents: str) -> bool:
    return "MongoClient" in file_contents


def detect_redis_calls(file_contents: str) -> bool:
    return "Redis(" in file_contents


def detect_gcp_calls(file_contents: str) -> bool:
    return "google.cloud" in file_contents or "from gcloud import " in file_contents


def describe_file_architecture(file_path: Path) -> str:
    with open(file_path, "r") as f:
        full_contents = f.read()

    checks = [
        detect_mongodb_calls,
        detect_boto3_calls,
        detect_requests_calls,
        detect_redis_calls,
        detect_gcp_calls,
    ]

    for arch_notifier in checks:
        if arch_notifier(full_contents):
            with open(file_path, "r") as f:
                contents = f.readlines()

            contents = [c.strip().strip("\n") for c in contents]
            return post("arch", contents)
