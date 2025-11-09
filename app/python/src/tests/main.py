import pytest

from ..db.tables import DynamoFenderTables
from ..main import handler
from ..models.models import SubscriptionAdapter
from ..schemas.schemas import EventSchema, SubscriptionEventPayload

CREATED_SUBSCRIPTION_EVENT = {
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

AWS_GET_EVENT_SUBSCRIPTION = {
    "resource": "/api/v1/subscriptions/{userId}",
    "path": "/api/v1/subscriptions/dummy_user",
    "httpMethod": "GET",
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "0s2r8aurv7.execute-api.us-east-1.amazonaws.com",
        "Postman-Token": "fa1c9874-89e9-4277-a5b1-e65017947519",
        "User-Agent": "PostmanRuntime/7.49.1",
        "X-Amzn-Trace-Id": "Root=1-690d790f-52e7f1510ea0af3242a5d1d6",
        "X-Forwarded-For": "189.179.129.75",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
    },
    "multiValueHeaders": {
        "Accept": ["*/*"],
        "Accept-Encoding": ["gzip, deflate, br"],
        "Host": ["0s2r8aurv7.execute-api.us-east-1.amazonaws.com"],
        "Postman-Token": ["fa1c9874-89e9-4277-a5b1-e65017947519"],
        "User-Agent": ["PostmanRuntime/7.49.1"],
        "X-Amzn-Trace-Id": ["Root=1-690d790f-52e7f1510ea0af3242a5d1d6"],
        "X-Forwarded-For": ["189.179.129.75"],
        "X-Forwarded-Port": ["443"],
        "X-Forwarded-Proto": ["https"],
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": {"userId": "123"},
    "stageVariables": None,
    "requestContext": {
        "resourceId": "xxxxyyy",
        "resourcePath": "/api/v1/subscriptions/{userId}",
        "httpMethod": "GET",
        "extendedRequestId": "Tp_ajGsBoAMEdCw=",
        "requestTime": "07/Nov/2025:04:43:59 +0000",
        "path": "/dev/api/v1/subscriptions/dummy_user",
        "accountId": "929676127859",
        "protocol": "HTTP/1.1",
        "stage": "dev",
        "domainPrefix": "xxxxxyyy",
        "requestTimeEpoch": 1762490639902,
        "requestId": "fb9a86bd-d6cf-4812-b69d-21f3ce009155",
        "identity": {
            "cognitoIdentityPoolId": None,
            "accountId": None,
            "cognitoIdentityId": None,
            "caller": None,
            "sourceIp": "189.179.129.75",
            "principalOrgId": None,
            "accessKey": None,
            "cognitoAuthenticationType": None,
            "cognitoAuthenticationProvider": None,
            "userArn": None,
            "userAgent": "PostmanRuntime/7.49.1",
            "user": None,
        },
        "domainName": "0s2r8aurv7.execute-api.us-east-1.amazonaws.com",
        "deploymentId": "w3dwr7",
        "apiId": "0s2r8aurv7",
    },
    "body": None,
    "isBase64Encoded": False,
}
AWS_POST_EVENT_SUBSCRIPTION = {
    "resource": "/api/v1/subscriptions/{userId}",
    "path": "/api/v1/subscriptions/dummy_user",
    "httpMethod": "POST",
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "0s2r8aurv7.execute-api.us-east-1.amazonaws.com",
        "Postman-Token": "fa1c9874-89e9-4277-a5b1-e65017947519",
        "User-Agent": "PostmanRuntime/7.49.1",
        "X-Amzn-Trace-Id": "Root=1-690d790f-52e7f1510ea0af3242a5d1d6",
        "X-Forwarded-For": "189.179.129.75",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
    },
    "multiValueHeaders": {
        "Accept": ["*/*"],
        "Accept-Encoding": ["gzip, deflate, br"],
        "Host": ["0s2r8aurv7.execute-api.us-east-1.amazonaws.com"],
        "Postman-Token": ["fa1c9874-89e9-4277-a5b1-e65017947519"],
        "User-Agent": ["PostmanRuntime/7.49.1"],
        "X-Amzn-Trace-Id": ["Root=1-690d790f-52e7f1510ea0af3242a5d1d6"],
        "X-Forwarded-For": ["189.179.129.75"],
        "X-Forwarded-Port": ["443"],
        "X-Forwarded-Proto": ["https"],
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": None,
    "stageVariables": None,
    "requestContext": {
        "resourceId": "xxxxyyy",
        "resourcePath": "/api/v1/subscriptions/{userId}",
        "httpMethod": "GET",
        "extendedRequestId": "Tp_ajGsBoAMEdCw=",
        "requestTime": "07/Nov/2025:04:43:59 +0000",
        "path": "/dev/api/v1/subscriptions/dummy_user",
        "accountId": "929676127859",
        "protocol": "HTTP/1.1",
        "stage": "dev",
        "domainPrefix": "xxxxxyyy",
        "requestTimeEpoch": 1762490639902,
        "requestId": "fb9a86bd-d6cf-4812-b69d-21f3ce009155",
        "identity": {
            "cognitoIdentityPoolId": None,
            "accountId": None,
            "cognitoIdentityId": None,
            "caller": None,
            "sourceIp": "189.179.129.75",
            "principalOrgId": None,
            "accessKey": None,
            "cognitoAuthenticationType": None,
            "cognitoAuthenticationProvider": None,
            "userArn": None,
            "userAgent": "PostmanRuntime/7.49.1",
            "user": None,
        },
        "domainName": "0s2r8aurv7.execute-api.us-east-1.amazonaws.com",
        "deploymentId": "w3dwr7",
        "apiId": "0s2r8aurv7",
    },
    "body": CREATED_SUBSCRIPTION_EVENT,
    "isBase64Encoded": False,
}


@pytest.mark.skip(reason="Skipping this test for now")
def test_handler_get_event():
    event = AWS_GET_EVENT_SUBSCRIPTION
    context = {}

    response = handler(event, context)


# @pytest.mark.skip(reason="Skipping this test for now")
def test_handler_post_event():
    event = AWS_POST_EVENT_SUBSCRIPTION
    context = {}

    response = handler(event, context)
    print(response)


@pytest.mark.skip(reason="Skipping this test for now")
def test_event_schema_get_method():
    event = EventSchema(**AWS_GET_EVENT_SUBSCRIPTION)
    assert event.is_get is True
    assert event.is_post is False

    event = EventSchema(**AWS_POST_EVENT_SUBSCRIPTION)
    assert event.is_get is False
    assert event.is_post is True


@pytest.mark.skip(reason="Skipping this test for now")
def test_subscription_event_creation():
    subscription_payload = SubscriptionEventPayload(**CREATED_SUBSCRIPTION_EVENT)

    assert subscription_payload.is_created is True
    assert subscription_payload.metadata.planSku == "PREMIUM_MONTHLY"
    assert subscription_payload.metadata.autoRenew is True
    assert subscription_payload.metadata.paymentMethod == "CREDIT_CARD"


@pytest.mark.skip(reason="Skipping this test for now")
def test_subscription_adapter():
    subscription_payload = SubscriptionEventPayload(**CREATED_SUBSCRIPTION_EVENT)
    adapter = SubscriptionAdapter(payload=subscription_payload)
    adapter.process()
