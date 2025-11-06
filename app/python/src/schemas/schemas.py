from dataclasses import dataclass
from enum import StrEnum


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class SubscriptionSchema:
    pk: str
    sk: str
    type: str
    planSku: str
    startDate: str
    expiresAt: str
    cancelledAt: str
    lastModified: str
    attributes: dict


@dataclass
class PlanSchema:
    pk: str
    sk: str
    type: str
    name: str
    price: float
    currency: str
    billingCycle: str
    features: list
    status: SubscriptionStatus
