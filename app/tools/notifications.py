"""Notification Microservice Connection"""

from langchain.tools import BaseTool
from typing import Optional, Type, Dict, Any
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from pydantic import BaseModel, Field, ValidationError
import os
import subprocess
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
TOPIC_ARN = os.getenv('TOPIC_ARN')

class NotificationInput(BaseModel):
    subject: str = Field(description="Subject of the notification email")
    message: str = Field(description="Message content of the notification email")

class NotificationTool(BaseTool):
    name = "notification"
    description = "Sends a notification email with a specified subject and message using a Node.js script."

    def _run(self, tool_input, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        try:
            # Log the received input
            print(f"Received tool_input: {tool_input}")

            # Attempt to parse the JSON string into a dictionary
            try:
                tool_input_dict = json.loads(tool_input)
                print(f"Parsed tool_input_dict: {tool_input_dict}")
            except json.JSONDecodeError as jde:
                return f"JSON decode error: {jde}"

            # Validate the parsed dictionary using the NotificationInput schema
            try:
                input_data = NotificationInput(**tool_input_dict)
            except ValidationError as ve:
                return f"Validation error: {ve}"

            subject = input_data.subject
            message = input_data.message

            # Construct the path to the Node.js script
            script_path = os.path.join(os.path.dirname(__file__), 'js', 'publish.js')

            # Execute the Node.js script with the necessary arguments
            result = subprocess.run(['node', script_path, TOPIC_ARN, subject, message], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Script executed successfully: {result.stdout}"
            else:
                return f"Error executing script: {result.stderr}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    async def _arun(self, tool_input: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")