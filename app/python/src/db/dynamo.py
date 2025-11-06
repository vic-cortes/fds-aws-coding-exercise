import boto3
from config import IS_DEVELOPMENT, Config


class DynamoFender:
    """
    DynamoDB connection handler for Fender application.
    """

    def __init__(self, tablename) -> None:
        if IS_DEVELOPMENT:
            auth_params = {
                "aws_access_key_id": Config.AWS_KEY_ID,
                "aws_secret_access_key": Config.AWS_KEY_SECRET,
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
