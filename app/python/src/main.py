from utils.response import success_response


def handler(event, context):
    print(f"{event=}, {context=}")
    return success_response("Fender Python Lambda is up and running!")
