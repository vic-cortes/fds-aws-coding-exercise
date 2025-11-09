import random
from enum import StrEnum
from typing import Literal

from faker import Faker
from pydantic import BaseModel

from ..db.tables import DynamoFenderTables
from ..schemas.schemas import SubscriptionEventPayload
from ..utils.response import success_response, validation_wrapper

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
    cancelledAt: str | None = None
    lastModified: str
    attributes: dict

    def create(self) -> None:
        DynamoFenderTables.SUBSCRIPTION.write(self.model_dump(exclude_none=True))


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
    lastModified: str | None = None

    def create(self) -> None:
        DynamoFenderTables.PLAN.write(self.model_dump())


class SubscriptionAdapter(BaseModel):
    payload: SubscriptionEventPayload

    def get(self) -> dict:
        return DynamoFenderTables.PLAN.get_by_pk(self.payload.metadata.planSku)

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

    def process(self) -> bool:
        if not self.get():
            self._create()


class PlanAdapter(BaseModel):
    payload: SubscriptionEventPayload

    def get(self) -> dict:
        return DynamoFenderTables.PLAN.get_by_pk(self.payload.metadata.planSku)

    def _create(self) -> None:
        """
        Process subscription event payload and create plan record.
        """
        DEFAULT_TYPE = "plan"
        DEFAULT_CURRENCY = "USD"
        # Random price and currency for demonstration purposes
        random_billing_cycle = random.choice(
            [BillingCycle.MONTHLY, BillingCycle.YEARLY]
        )
        random_features = [f"Feature {el}" for el in fake.random_sample()]
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
            "lastModified": self.payload.timestamp,
        }
        plan_model = PlanModel(**data)
        plan_model.create()

    def process(self) -> None:
        if not self.get():
            return self._create()


@validation_wrapper
def process_subscription_and_plan(payload: SubscriptionEventPayload) -> None:
    plan_adapter = PlanAdapter(payload=payload)
    plan_adapter.process()

    subscription_adapter = SubscriptionAdapter(payload=payload)
    subscription_adapter.process()
    return success_response("Subscription and Plan processed successfully")
