from http import HTTPStatus


def handler(event, context):
    return {
        "statusCode": HTTPStatus.OK,
        "body": "Hello from Python Lambda!",
    }
