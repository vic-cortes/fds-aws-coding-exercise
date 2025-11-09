from pydantic import BaseModel

try:
    # For local development
    from .models.models import process_subscription_and_plan, process_user_id
    from .schemas.schemas import EventSchema, SubscriptionEventPayload
    from .utils.response import error_response
except:
    # For AWS Lambda deployment
    from models.models import process_subscription_and_plan, process_user_id
    from schemas.schemas import EventSchema, SubscriptionEventPayload
    from utils.response import error_response


def router_get_user_subscription(user_id: str) -> dict:
    return process_user_id(user_id=user_id)


def router_post_user_subscription(body: SubscriptionEventPayload) -> dict:
    return process_subscription_and_plan(payload=body)


class Router(BaseModel):
    event: EventSchema

    def process_event(self) -> dict:

        if self.event.is_get:
            user_id = self.event.pathParameters.userId
            return router_get_user_subscription(user_id=user_id)

        elif self.event.is_post:
            body = SubscriptionEventPayload(**self.event.body)
            return router_post_user_subscription(body=body)

        else:
            return error_response("Unsupported HTTP method", status_code=405)
