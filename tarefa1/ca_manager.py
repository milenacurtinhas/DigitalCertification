import datetime
import ipaddress

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509
from cryptography.hazmat.primitives import hashes

import files_manager

def create_root_ca():
    root_key = rsa.generate_private_key(public_exponent=65537, key_size=4096) 

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'BR'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Espirito Santo'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'Vitoria'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Organização fictícia'),
        x509.NameAttribute(NameOID.COMMON_NAME, 'Root CA'),
    ])

    root_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        root_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Validade de 10 anos
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365*10)
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False, 
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False
        ),
        critical=True,
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(root_key.public_key()),
        critical=False,
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(root_key.public_key()),
        critical=False,
    ).sign(root_key, hashes.SHA256())

    folder_path = files_manager.create_folder('root')
    files_manager.save_key(root_key, folder_path, 'root_key')
    files_manager.save_pem(root_cert, folder_path, 'root_cert', extension='pem')

    return root_cert, root_key


def create_intermediate_ca(root_cert, root_key):
    intermediate_key = rsa.generate_private_key(public_exponent=65537, key_size=4096) 

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'BR'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Espirito Santo'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'Vitoria'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Organização fictícia'),
        x509.NameAttribute(NameOID.COMMON_NAME, 'Intermediate CA'),
    ])

    intermediate_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        root_cert.subject
    ).public_key(
        intermediate_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Validade de 3 anos
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365*3)
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=0),
        critical=True,
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(intermediate_key.public_key()),
        critical=False,
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
            root_cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value
        ),
        critical=False,
    ).sign(root_key, hashes.SHA256())

    folder_path = files_manager.create_folder('intermediate')
    files_manager.save_pem(intermediate_cert, folder_path, 'intermediate_cert', extension='pem')
    files_manager.save_key(intermediate_key, folder_path, 'intermediate_key')
        
    return intermediate_cert, intermediate_key

def issue_certificate(ca, ca_key):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Certificate Signing Request
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'BR'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Espirito Santo'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'Vitoria'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Organização fictícia'),
        x509.NameAttribute(NameOID.COMMON_NAME, 'localhost'),
    ])).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName('localhost'),
            x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # Sign Certificate 
    server_cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Validade de 100 dias
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=100)
    ).add_extension(
        csr.extensions.get_extension_for_class(x509.SubjectAlternativeName).value,
        critical=False,
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=True,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    ).add_extension(
        x509.ExtendedKeyUsage([x509.ExtendedKeyUsageOID.SERVER_AUTH]),
        critical=False,
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(csr.public_key()),
        critical=False,
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
            ca.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value
        ),
        critical=False,
    ).sign(ca_key, hashes.SHA256())

    folder_path = files_manager.create_folder('server')
    files_manager.save_key(key, folder_path, 'server_key')
    files_manager.save_pem(csr, folder_path, 'csr', extension='csr')
    files_manager.save_pem(server_cert, folder_path, 'server_cert', extension='crt')

    return server_cert