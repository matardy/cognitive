from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, Field, ValidationError
import boto3
import json
import os
from io import BytesIO
from botocore.client import Config
from botocore import UNSIGNED
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from dotenv import load_dotenv
load_dotenv()
BUCKET_S3 = os.getenv('BUCKET_S3')
AWS_REGION = os.getenv('AWS_REGION')

# Configuración de Boto3 para acceso sin firmar
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED), region_name=AWS_REGION)

class S3ToolInput(BaseModel):
    action: str = Field(description="Action to perform: list, get, or put")
    object_key: Optional[str] = Field(default=None, description="Key of the S3 object")
    content: Optional[str] = Field(default=None, description="Text content to upload as a .txt file")

class S3Tool(BaseTool):
    name = "s3_tool"
    description = "Interacts with S3 to list, retrieve and upload objects as .txt files directly from text."
    args_schema: Type[BaseModel] = S3ToolInput
    bucket_name = BUCKET_S3  # Default bucket name

    def _run(self, tool_input, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        try:
            # Parse tool input
            tool_input_dict = json.loads(tool_input)
            input_data = S3ToolInput(**tool_input_dict)
            action = input_data.action

            if action == 'list':
                return self.list_bucket_contents()
            elif action == 'get' and input_data.object_key:
                return self.get_object_text(input_data.object_key)
            elif action == 'put' and input_data.object_key and input_data.content:
                return self.upload_text_as_file(input_data.content, input_data.object_key)
            else:
                return "Invalid input or missing parameters for the requested action."

        except ValidationError as ve:
            return f"Validation error: {ve}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def list_bucket_contents(self):
        try:
            response = s3.list_objects_v2(Bucket=self.bucket_name)
            contents = [f'Key: {item["Key"]}, Last Modified: {item["LastModified"]}, Size: {item["Size"]}' for item in response.get('Contents', [])]
            return "\n".join(contents)
        except Exception as e:
            return f"Error listing bucket contents: {e}"

    def get_object_text(self, object_key):
        try:
            response = s3.get_object(Bucket=self.bucket_name, Key=object_key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            return f"Error retrieving object text: {e}"

    def upload_text_as_file(self, content, object_key):
        try:
            file_stream = BytesIO(content.encode('utf-8'))
            s3.put_object(Bucket=self.bucket_name, Key=object_key, Body=file_stream)
            return f'Text content uploaded to {self.bucket_name} as {object_key}'
        except NoCredentialsError:
            return "Credentials not available"
        except PartialCredentialsError:
            return "Incomplete credentials"
        except Exception as e:
            return f"Error uploading text content: {e}"
