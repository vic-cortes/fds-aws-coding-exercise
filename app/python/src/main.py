from utils.response import success_response

from .schemas.schemas import EventSchema


def handler(event, context):
    event = EventSchema(**event)
    return success_response("Fender Python Lambda is up and running!")
