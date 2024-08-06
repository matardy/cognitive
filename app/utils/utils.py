from cryptography.fernet import Fernet

def encrypt_message(message: str, secret_key: str) -> str:
    fernet = Fernet(secret_key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt_message(encrypted_message: str, secret_key: str) -> str:
    fernet = Fernet(secret_key)
    decrypted_message = fernet.decrypt(encrypted_message.encode())
    return decrypted_message.decode()