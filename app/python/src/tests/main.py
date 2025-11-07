import pytest

from ..schemas.schemas import SubscriptionEvent

SAMPLE_DATA = {
    "eventId": "evt_123456789",
    "eventType": "subscription.created",
    "timestamp": "2024-03-20T10:00:00Z",
    "provider": "STRIPE",
    "subscriptionId": "sub_456789",
    "paymentId": "pm_123456",
    "userId": "123",
    "customerId": "cus_789012",
    "expiresAt": "2024-04-20T10:00:00Z",
    "metadata": {
        "planSku": "PREMIUM_MONTHLY",
        "autoRenew": True,
        "paymentMethod": "CREDIT_CARD",
    },
}


def test_subscription_event_creation():
    subscription_event = SubscriptionEvent(**SAMPLE_DATA)

    assert subscription_event.is_created is True
    assert subscription_event.metadata.planSku == "PREMIUM_MONTHLY"
    assert subscription_event.metadata.autoRenew is True
    assert subscription_event.metadata.paymentMethod == "CREDIT_CARD"
