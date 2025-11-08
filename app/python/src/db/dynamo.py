import json

import boto3
from boto3.dynamodb.conditions import And, Key

from ..config import IS_DEVELOPMENT, Config


def serialize_dynamo(dict):
    return json.loads(json.dumps(dict, default=str_dynamo_data))


def str_dynamo_data(obj):
    # Coerce every object into string
    return str(obj)


class DynamoFender:
    """
    DynamoDB connection handler for Fender application.
    """

    def __init__(self, tablename) -> None:
        if IS_DEVELOPMENT:
            auth_params = {
                "aws_access_key_id": Config.AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": Config.AWS_SECRET_ACCESS_KEY,
                "region_name": Config.AWS_REGION_NAME,
            }
            self.dynamodb = boto3.resource("dynamodb", **auth_params)
            self.client = boto3.client("dynamodb", **auth_params)
        else:
            self.dynamodb = boto3.resource("dynamodb")
            self.client = boto3.client("dynamodb")
        try:
            self.table = self.dynamodb.Table(tablename)
        except Exception as error:
            raise ValueError(
                f"Could't make connection to `{tablename}` table due `{error}`"
            )

    def write(self, data: list | dict) -> bool:
        """
        Writes data into table
        """

        if isinstance(data, dict):
            data = [data]

        with self.table.batch_writer() as batch:
            for values in data:
                batch.put_item(Item=values)

        return True

    def get_by_pk(self, pk: str) -> dict:
        response = self.table.query(KeyConditionExpression=Key("pk").eq(pk))
        return serialize_dynamo(response["Items"])

    def get_or_create(self, pk: str, sk: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=And(Key("pk").eq(pk), Key("sk").eq(sk))
        )
        items = serialize_dynamo(response["Items"])
        if items:
            return items[0]
        return {}


class SubscriptionTable(DynamoFender):
    """
    DynamoDB handler for Subscription table.
    """

    __tablename__ = "FenderSubscriptions"

    def __init__(self, tablename: str = None) -> None:
        _tablename = tablename or self.__tablename__
        super().__init__(_tablename)


class PlanTable(DynamoFender):
    """
    DynamoDB handler for Plan table.
    """

    __tablename__ = "FenderPlans"

    def __init__(self, tablename: str = None) -> None:
        _tablename = tablename or self.__tablename__
        super().__init__(_tablename)
