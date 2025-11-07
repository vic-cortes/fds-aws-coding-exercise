from .routes import Router
from .schemas.schemas import EventSchema
from .utils.response import success_response


def handler(event, context):
    event = EventSchema(**event)
    router = Router(event=event)

    return router.process_event()
