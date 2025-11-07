from .dynamo import PlanTable, SubscriptionTable


class DynamoFenderTables:
    SUBSCRIPTION = SubscriptionTable()
    PLAN = PlanTable()
