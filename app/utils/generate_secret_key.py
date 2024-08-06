from cryptography.fernet import Fernet
new_key = Fernet.generate_key()
print(new_key.decode())