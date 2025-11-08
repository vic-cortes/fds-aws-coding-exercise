from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from ..db.tables import DynamoFenderTables
from ..schemas.schemas import SubscriptionEventPayload


class BillingCycle(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PlanStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SubscriptionModel(BaseModel):
    pk: str
    sk: str
    type: str = "sub"
    planSku: str
    startDate: str
    expiresAt: str
    cancelledAt: str | None
    lastModified: str
    attributes: dict


class PlanModel(BaseModel):
    pk: str
    sk: str
    type: str
    name: str
    price: float
    currency: str
    billingCycle: Literal[BillingCycle.MONTHLY, BillingCycle.YEARLY]
    features: list[str]
    status: Literal[PlanStatus.ACTIVE, PlanStatus.INACTIVE]


class SubscriptionAdapter(BaseModel):
    payload: SubscriptionEventPayload

    def get_or_create(self) -> None:
        DynamoFenderTables.SUBSCRIPTION.get_by_pk(self.payload.pk)

    def create(self, data: SubscriptionModel) -> None:
        data = {"pk": self.payload.pk}
        SubscriptionModel(**data)


class PlanAdapter(BaseModel):
    payload: SubscriptionEventPayload

    def create(self, data: PlanModel) -> None:
        pass


class SubscriptionPlanModel(BaseModel):
    """
    Determines the data model for both Subscription and Plan.
    """

    payload: SubscriptionEventPayload
