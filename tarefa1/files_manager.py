from pathlib import Path
from cryptography.hazmat.primitives import serialization

def create_folder(folder_name):
    folder_path = Path(f'tarefa1/ca_storage/{folder_name}')

    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied: Unable to create directory '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return folder_path

def save_pem(file, folder_path, file_name, extension):
    file_path = folder_path/f'{file_name}.{extension}'
    try:
        with open(file_path, 'wb') as f:
            f.write(file.public_bytes(serialization.Encoding.PEM))
    except Exception as e:
        print(f"An error occurred while saving {file_path}: {e}")

def save_key(key, folder_path, file_name):
    file_path = folder_path/f'{file_name}.key'
    try:
        with open(file_path, 'wb') as f:
            f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL, 
                    encryption_algorithm=serialization.NoEncryption(),
            ))
    except Exception as e:
        print(f"An error occurred while saving {file_path}: {e}")
     