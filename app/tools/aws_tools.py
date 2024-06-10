import boto3 
from dotenv import load_dotenv
import os 
from botocore import UNSIGNED
from botocore.client import Config
import requests
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

def publicar_mensaje(subject, message, topic_arn=TOPIC_ARN):
    url = "https://sns.us-east-1.amazonaws.com/"
    data = {
        "Action": "Publish",
        "TopicArn": topic_arn,
        "Message": message,
        "Subject": subject,
        "Version": "2010-03-31"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Mensaje publicado:', response.text)
    else:
        print('Error al publicar mensaje:', response.text)

if __name__ == "__main__":
    subject = 'python test'
    message = 'this is a test from a python script'
    publish_message(subject=subject, message=message)
    publicar_mensaje(subject=subject, message=message)