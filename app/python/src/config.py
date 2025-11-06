import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    AWS_KEY_ID = os.getenv("AWS_KEY_ID", "")
    AWS_KEY_SECRET = os.getenv("AWS_KEY_SECRET", "")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")


IS_DEVELOPMENT = Config.ENVIRONMENT == "development"
