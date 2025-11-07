from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SubscriptionType(StrEnum):
    RENEWAL = "subscription.renewed"
    CREATED = "subscription.created"
    CANCELLED = "subscription.cancelled"


class SupportedMethods(StrEnum):
    GET = "GET"
    POST = "POST"


class EventSchema(BaseModel):
    httpMethod: str

    @property
    def is_get(self) -> bool:
        return self.httpMethod == SupportedMethods.GET

    @property
    def is_post(self) -> bool:
        return self.httpMethod == SupportedMethods.POST


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
    cancelledAt: str | None
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
    status: Literal[SubscriptionStatus.ACTIVE, SubscriptionStatus.INACTIVE]
