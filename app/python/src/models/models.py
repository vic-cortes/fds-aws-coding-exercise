from pydantic import BaseModel

from ..schemas.schemas import PlanSchema, SubscriptionEventPayload, SubscriptionSchema


class SubscriptionModel(BaseModel):
    payload: SubscriptionEventPayload

    def create(self, data: SubscriptionSchema) -> None:
        pass


class PlanModel(BaseModel):
    payload: SubscriptionEventPayload

    def create(self, data: PlanSchema) -> None:
        pass


class SubscriptionPlanModel(BaseModel):
    """
    Determines the data model for both Subscription and Plan.
    """

    payload: SubscriptionEventPayload
