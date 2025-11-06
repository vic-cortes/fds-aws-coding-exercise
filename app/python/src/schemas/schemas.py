from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SubscriptionSchema(BaseModel):
    pk: str
    sk: str
    type: str
    planSku: str
    startDate: str
    expiresAt: str
    cancelledAt: str
    lastModified: str
    attributes: dict


class PlanSchema(BaseModel):
    pk: str
    sk: str
    type: str
    name: str
    price: float
    currency: str
    billingCycle: str
    features: list
    status: Annotated[
        list[SubscriptionStatus],
        SubscriptionStatus.ACTIVE | SubscriptionStatus.INACTIVE,
    ]
