from pathlib import Path
from cryptography.hazmat.primitives import serialization


def create_folder(folder_name):
    """
    Função que cria uma nova pasta para armezar os arquivos.
    :param folder_name: nome da pasta a ser criada
    :return: retorna o caminho da nova pasta
    """
    folder_path = Path(f'ca_storage/{folder_name}')

    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied: Unable to create directory '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return folder_path

def save_pem(file, folder_path, file_name, extension):
    """
    Função que salva em disco um objeto (Certificado ou CSR) codificado em PEM.
    A extensão é recebida por parâmetro (ex: 'csr', 'crt', 'pem').
    :param file: arquivoa ser codificado
    :param folder_path: caminho da pasta onde a chave será salva
    :param file_name: nome do arquivo a ser salvo
    :param extension: extensão do arquivo a ser salvo 
    """
    file_path = folder_path/f'{file_name}.{extension}'
    try:
        with open(file_path, 'wb') as f:
            f.write(file.public_bytes(serialization.Encoding.PEM))
    except Exception as e:
        print(f"An error occurred while saving {file_path}: {e}")

def save_key(key, folder_path, file_name):
    """
   Função que salva em disco a chave privada codificada em PEM, 
    usando o formato tradicional do OpenSSL e sem criptografia.
    A extensão é fixa ('key').
    :param key: chave privada a ser salva
    :param folder_path: caminho da pasta onde a chave será salva
    :param file_name: nome do arquivo (sem extensão)
    """
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
     