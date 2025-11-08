from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from ..utils.utils import parse_iso8601


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    PENDING = "pending"
    CANCELLED = "cancelled"


class SubscriptionType(StrEnum):
    RENEWAL = "subscription.renewed"
    CREATED = "subscription.created"
    CANCELLED = "subscription.cancelled"


class SupportedMethods(StrEnum):
    GET = "GET"
    POST = "POST"


class EventSchema(BaseModel):
    httpMethod: str
    path: str
    body: Optional[dict] = None
    pathParameters: Optional[dict] = None

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
    def _current_datetime(self) -> datetime:
        return datetime.now(timezone.utc)

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

    @property
    def parse_cancelledAt(self) -> str | None:
        if self.cancelledAt:
            return parse_iso8601(self.cancelledAt)

    @property
    def is_pending(self) -> bool:
        return self._current_datetime <= self.parse_cancelledAt

    @property
    def is_cancelled(self) -> bool:
        return self._current_datetime > self.parse_cancelledAt

    @property
    def compute_status(self) -> SubscriptionStatus:
        if not self.cancelledAt:
            return SubscriptionStatus.ACTIVE
        if self.is_pending:
            return SubscriptionStatus.PENDING
        if self.is_cancelled:
            return SubscriptionStatus.CANCELLED
