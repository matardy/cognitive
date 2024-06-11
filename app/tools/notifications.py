from langchain.tools import BaseTool
from typing import Optional, Type, Dict
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from pydantic import BaseModel, Field
import os
import subprocess
from dotenv import load_dotenv
asdasdasd
# Load environment variables
load_dotenv()
TOPIC_ARN = os.getenv('TOPIC_ARN')

class NotificationInput(BaseModel):
    subject: str = Field(description="Subject of the notification email")
    message: str = Field(description="Message content of the notification email")

class NotificationTool(BaseTool):
    name = "notification"
    description = "Sends a notification email with a specified subject and message using a Node.js script."
    args_schema: Type[BaseModel] = NotificationInput

    def _run(self, tool_input: Dict[str, str], run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        try:
            subject = tool_input.get('subject')
            message = tool_input.get('message')
            script_path = os.path.join(os.path.dirname(__file__), 'js', 'publish.js')
            result = subprocess.run(['node', script_path, TOPIC_ARN, subject, message], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f'Script executed successfully: {result.stdout}'
            else:
                return f'Error executing script: {result.stderr}'
        except Exception as e:
            return f'An error occurred: {e}'

    async def _arun(self, tool_input: Dict[str, str], run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")
