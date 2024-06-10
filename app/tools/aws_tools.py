import boto3 
from dotenv import load_dotenv
import os 
from botocore import UNSIGNED
from botocore.client import Config
load_dotenv()

TOPIC_ARN = os.getenv('TOPIC_ARN') 

def publish_message(subject, message):
    sns_client = boto3.client('sns', config=Config(signature_version=UNSIGNED), region_name = 'us-east-1')

    response = sns_client.publish(
        TopicArn = TOPIC_ARN,
        Message = message,
        Subject = subject
    )

    print("Message Published succesfully")
    return response

if __name__ == "__main__":
    subject = 'python test'
    message = 'this is a test from a python script'
    publish_message(subject=subject, message=message)