from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime, timezone

def load_cert(path):
    with open(path, "rb") as f:
        # Carrega o certificado X.509 no formato PEM
        return x509.load_pem_x509_certificate(f.read())

def verify_signature(cert, issuer_cert):
    """
    Verifica se 'cert' foi assinado pela chave privada de 'issuer_cert'.
    """
    issuer_public_key = issuer_cert.public_key()
    
    try:
        # A verificação depende do algoritmo de assinatura (normalmente RSA com PKCS1v15)
        # O método tbs_certificate_bytes fornece os dados brutos que foram assinados
        issuer_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(), # Padrão para certificados X.509
            cert.signature_hash_algorithm
        )
        print(f"Assinatura OK: {cert.subject} assinado por {issuer_cert.subject}")
    except Exception as e:
        raise Exception(f"Falha na assinatura para {cert.subject}: {e}")

def check_validity(cert):
    """Verifica se o certificado está válido no tempo (não expirado)."""
    now = datetime.now(timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        raise Exception(f"Certificado expirado ou ainda não válido: {cert.subject}")

# --- Fluxo Principal ---

# Caminhos
server_cert_path = "ca_storage/server/server_cert.crt"
intermediate_cert_path = "ca_storage/intermediate/intermediate_cert.pem"
root_cert_path = "ca_storage/root/root_cert.pem"

try:
    # 1. Carregar certificados
    server_cert = load_cert(server_cert_path)
    intermediate_cert = load_cert(intermediate_cert_path)
    root_cert = load_cert(root_cert_path)

    # 2. Validar Datas
    check_validity(server_cert)
    check_validity(intermediate_cert)
    check_validity(root_cert)

    # 3. Validar a Cadeia (Chain of Trust)
    # Passo A: Verificar se o Server foi assinado pelo Intermediate
    verify_signature(server_cert, intermediate_cert)

    # Passo B: Verificar se o Intermediate foi assinado pelo Root
    verify_signature(intermediate_cert, root_cert)
    
    # Passo C (Opcional): Verificar se o Root é auto-assinado (confiável por si só)
    # Em sistemas reais, você confia no Root porque você o possui, não apenas pela assinatura.
    verify_signature(root_cert, root_cert)

    print("\nCadeia de certificação completa: OK")

except Exception as e:
    print(f"\nErro na validação da cadeia: {e}")