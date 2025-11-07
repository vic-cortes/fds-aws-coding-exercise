import json
from http import HTTPStatus


def success_response(body: str) -> dict:
    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({"message": body}),
    }
