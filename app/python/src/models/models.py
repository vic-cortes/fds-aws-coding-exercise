from ..schemas.schemas import PlanSchema, SubscriptionEventPayload, SubscriptionSchema


class SubscriptionModel:

    def create(self, data: SubscriptionSchema) -> None:
        pass


class PlanModel:

    def create(self, data: PlanSchema) -> None:
        pass


class SubscriptionPlanModel:
    payload: SubscriptionEventPayload
