from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import boto3
from pydantic import BaseModel, Field
import os
from botocore.config import Config
from botocore.handlers import disable_signing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOPIC_ARN = os.getenv('TOPIC_ARN')

class NotificationInput(BaseModel):
    subject: str = Field(description="Subject of the notification email")
    message: str = Field(description="Message content of the notification email")

class NotificationTool(BaseTool):
    name = "notification"
    description = "Sends a notification email with a specified subject and message."
    args_schema: Type[BaseModel] = NotificationInput

    def _run(self, subject: str, message: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        sns_client = boto3.client('sns', config=Config(signature_version='UNSIGNED'), region_name='us-east-1')

        response = sns_client.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject=subject
        )

        return f"Message Published successfully: {response}"

    async def _arun(self, subject: str, message: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")
