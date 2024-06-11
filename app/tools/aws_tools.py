import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore import UNSIGNED
from botocore.client import Config

# Inicializa el cliente de S3
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED), region_name='us-east-1')  # Cambia la región según necesites

def list_bucket_contents(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for item in response.get('Contents', []):
            print(f'Key: {item["Key"]}, Last Modified: {item["LastModified"]}, Size: {item["Size"]}')
    except Exception as e:
        print(f"Error listing bucket contents: {e}")

def get_object_text(bucket_name, object_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error retrieving object text: {e}")

def upload_file_to_bucket(bucket_name, file_path, object_name):
    try:
        with open(file_path, 'rb') as file:
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=file)
        print(f'File {file_path} uploaded to {bucket_name} as {object_name}')
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Uso de las funciones
bucket_name = 'cognitive-ai-bucket'  # Asegúrate de usar el nombre correcto de tu bucket

# Listar contenido
list_bucket_contents(bucket_name)

# # Obtener texto de un objeto específico
object_key = 'test.txt'  # Cambia esto por la clave real del objeto en tu bucket
print(get_object_text(bucket_name, object_key))

# # Subir un nuevo archivo
# file_path = 'path/to/your/file.txt'  # Ruta al archivo que quieres subir
# upload_file_to_bucket(bucket_name, file_path, 'new-file-name.txt')  # Nombre bajo el cual el archivo se guardará en el bucket
