from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SubscriptionType(StrEnum):
    RENEWAL = "subscription.renewed"
    CREATED = "subscription.created"
    CANCELLED = "subscription.cancelled"


class MetadataSchema(BaseModel):
    planSku: str
    autoRenew: bool
    paymentMethod: str


class SubscriptionEvent(BaseModel):
    eventId: str
    eventType: str
    timestamp: str
    provider: str
    subscriptionId: str
    paymentId: str
    userId: str
    customerId: str
    expiresAt: str
    metadata: MetadataSchema

    @property
    def is_renewal(self) -> bool:
        return self.eventType == SubscriptionType.RENEWAL

    @property
    def is_created(self) -> bool:
        return self.eventType == SubscriptionType.CREATED

    @property
    def is_cancelled(self) -> bool:
        return self.eventType == SubscriptionType.CANCELLED


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
