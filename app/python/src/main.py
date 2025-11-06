from src.utils.response import success_response


def handler(event, context):
    return success_response("Fender Python Lambda is up and running!")
