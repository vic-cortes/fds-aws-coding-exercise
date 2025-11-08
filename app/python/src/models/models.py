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

    def create(self) -> None:
        DynamoFenderTables.SUBSCRIPTION.write(self.model_dump())


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

    def _create(self) -> None:
        """
        Process subscription event payload and create subscription record.
        """
        DEFAULT_TYPE = "sub"
        data = {
            "pk": self.payload.userId,
            "sk": self.payload.subscriptionId,
            "type": DEFAULT_TYPE,
            "planSku": self.payload.metadata.planSku,
            "startDate": self.payload.timestamp,
            "expiresAt": self.payload.expiresAt,
            "cancelledAt": self.payload.cancelledAt,
            "lastModified": self.payload.timestamp,
            "attributes": {
                "provider": self.payload.provider,
                "paymentId": self.payload.paymentId,
                "customerId": self.payload.customerId,
                "autoRenew": self.payload.metadata.autoRenew,
                "paymentMethod": self.payload.metadata.paymentMethod,
            },
        }
        subscription_model = SubscriptionModel(**data)
        subscription_model.create()

    def process(self) -> None:
        self._create()


class PlanAdapter(BaseModel):
    payload: SubscriptionEventPayload

    def create(self, data: PlanModel) -> None:
        pass
