from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class SubscriptionType(StrEnum):
    RENEWAL = "subscription.renewed"
    CREATED = "subscription.created"
    CANCELLED = "subscription.cancelled"


class SupportedMethods(StrEnum):
    GET = "GET"
    POST = "POST"


class UserParamsSchema(BaseModel):
    userId: str


class EventSchema(BaseModel):
    httpMethod: str
    path: str
    body: Optional[dict] = None
    pathParameters: Optional[UserParamsSchema] = None

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


class SubscriptionEventPayload(BaseModel):
    eventId: str
    eventType: str
    timestamp: str
    provider: str
    subscriptionId: str
    paymentId: str
    userId: str
    customerId: str
    expiresAt: str
    cancelledAt: Optional[str] = None
    metadata: MetadataSchema

    @property
    def plan_name(self) -> str:
        return self.metadata.planSku.replace("_", " ").title()

    @property
    def is_renewal(self) -> bool:
        return self.eventType == SubscriptionType.RENEWAL

    @property
    def is_created(self) -> bool:
        return self.eventType == SubscriptionType.CREATED

    @property
    def is_cancelled(self) -> bool:
        return self.eventType == SubscriptionType.CANCELLED
