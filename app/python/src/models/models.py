import random
from enum import StrEnum
from typing import Literal

from faker import Faker
from pydantic import BaseModel

from ..db.tables import DynamoFenderTables
from ..schemas.schemas import SubscriptionEventPayload

fake = Faker("es_MX")


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
        DynamoFenderTables.SUBSCRIPTION.write(self.model_dump(ignore_none=True))


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

    def create(self) -> None:
        """
        Process subscription event payload and create plan record.
        """
        DEFAULT_TYPE = "plan"
        DEFAULT_CURRENCY = "USD"
        # Random price and currency for demonstration purposes
        random_billing_cycle = random.choice(
            [BillingCycle.MONTHLY, BillingCycle.YEARLY]
        )
        random_features = [f"feature {el}" for el in fake.random_sample()]
        data = {
            "pk": self.payload.metadata.planSku,
            "sk": self.payload.metadata.paymentMethod,
            "type": DEFAULT_TYPE,
            "name": self.payload.plan_name,
            "price": float(fake.numerify()),
            "currency": DEFAULT_CURRENCY,
            "billingCycle": random_billing_cycle,
            "features": random_features,
            "status": PlanStatus.ACTIVE,
        }
        plan_model = PlanModel(**data)
        DynamoFenderTables.PLAN.write(plan_model.model_dump())
