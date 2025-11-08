import boto3

from ..config import IS_DEVELOPMENT, Config
from ..schemas.schemas import SubscriptionSchema


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

    def write(self, data: list) -> bool:
        """
        Writes data into table
        """

        if not data:
            raise ValueError("Data cannot be empty or null")

        if not isinstance(data, list):
            raise ValueError(f"Data must be type `list`, given `{type(data)}`")

        with self.table.batch_writer() as batch:
            for values in data:
                batch.put_item(Item=values)

        return True


class SubscriptionTable(DynamoFender):
    """
    DynamoDB handler for Subscription table.
    """

    __tablename__ = "FenderSubscriptions"

    def __init__(self, tablename: str = None) -> None:
        _tablename = tablename or self.__tablename__
        super().__init__(_tablename)

    def write(self, data: SubscriptionSchema) -> bool:
        return super().write(data.model_dump())


class PlanTable(DynamoFender):
    """
    DynamoDB handler for Plan table.
    """

    __tablename__ = "FenderPlans"

    def __init__(self, tablename: str = None) -> None:
        _tablename = tablename or self.__tablename__
        super().__init__(_tablename)
