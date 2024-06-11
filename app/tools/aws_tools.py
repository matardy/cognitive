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


def ejecutar_script_js(subject, message, topic_arn=TOPIC_ARN):
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'js', 'publish.js')
        print(os.path.dirname(__file__))
        print(script_path)
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