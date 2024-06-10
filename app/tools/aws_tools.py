import boto3 
from dotenv import load_dotenv
import os 
from botocore import UNSIGNED
from botocore.client import Config
import requests
from botocore.handlers import disable_signing
import subprocess
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

def publicar_mensaje_request(topic_arn, subject, message):
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

def publicar_mensaje(topic_arn, subject, message, region_name):
    # Create the SNS resource with unsigned configuration
    sns = boto3.resource('sns', region_name=region_name, config=Config(signature_version=UNSIGNED))

    # Disable signing for the client
    sns.meta.client.meta.events.register('choose-signer.sns.*', disable_signing)

    # Get the topic by its ARN
    topic = sns.Topic(topic_arn)

    # Publish a message to the topic
    response = topic.publish(
        Message=message,
        Subject=subject
    )

    print('Mensaje publicado:', response)
    return response

def ejecutar_script_js(subject, message, topic_arn=TOPIC_ARN,):
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'js', 'publish.js')
        print(os.path.dirname(__file__))
        # Ejecutar el script de JavaScript usando Node.js con argumentos
        result = subprocess.run(['node', script_path, topic_arn, subject, message], capture_output=True, text=True)
        
        # Verificar la salida
        if result.returncode == 0:
            print('Script ejecutado correctamente')
            print('Salida:', result.stdout)
        else:
            print('Error al ejecutar el script')
            print('Error:', result.stderr)
    except Exception as e:
        print(f'Ocurrió un error: {e}')

if __name__ == "__main__":
    subject = 'python test'
    message = 'this is a test from a python script'
    ejecutar_script_js(subject=subject, message=message)