from pydantic import BaseModel

from .schemas.schemas import EventSchema, SubscriptionEventPayload
from .utils.response import success_response


class Router(BaseModel):
    event: EventSchema

    def get_user_subscription(self) -> str | None:
        pass

    def post_user_subscription(self, body: SubscriptionEventPayload) -> None:
        # TODO: Add DynamoDB logic to store the subscription event
        pass

    def process_event(self) -> dict:

        if self.event.is_get:
            return success_response("GET method processed successfully")

        elif self.event.is_post:
            body = SubscriptionEventPayload(**self.event.body)
            self.post_user_subscription(body=body)

        else:
            raise ValueError("Unsupported HTTP method")
