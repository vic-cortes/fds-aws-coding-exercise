try:
    # For local development
    from .dynamo import PlanTable, SubscriptionTable
except:
    # For AWS Lambda deployment
    from dynamo import PlanTable, SubscriptionTable


class DynamoFenderTables:
    SUBSCRIPTION = SubscriptionTable()
    PLAN = PlanTable()
