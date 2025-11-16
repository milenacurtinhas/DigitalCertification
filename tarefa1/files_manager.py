from pathlib import Path
from cryptography.hazmat.primitives import serialization

def create_folder(folder_name):
    folder_path = Path(f'ca_storage/{folder_name}')

    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print(f"Directory '{folder_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create directory '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return folder_path

def save_pem(file, folder_path, file_name, extension):
    with open(f'{folder_path}/{file_name}.{extension}', 'wb') as f:
        f.write(file.public_bytes(serialization.Encoding.PEM))

def save_key(key, folder_path, file_name):
    with open(f'{folder_path}/{file_name}.key', 'wb') as f:
     f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL, 
            encryption_algorithm=serialization.NoEncryption(),
        ))
     