#!/bin/bash

set -e

echo "========================================"
echo "Gerando Certificado do Servidor"
echo "========================================"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}[1/3] Gerando chave privada do servidor (RSA 2048 bits)...${NC}"
openssl genrsa -out ca-intermediate/private/server.key 2048
chmod 400 ca-intermediate/private/server.key
echo -e "${GREEN}✓ Chave privada do servidor gerada${NC}"

echo -e "\n${BLUE}[2/3] Criando CSR do servidor...${NC}"
openssl req -config openssl-ca-intermediate.cnf \
    -new -sha256 \
    -key ca-intermediate/private/server.key \
    -out ca-intermediate/csr/server.csr \
    -subj "/C=BR/ST=ES/L=Vitoria/O=UFES/OU=DI/CN=localhost"
echo -e "${GREEN}✓ CSR do servidor criado${NC}"

echo -e "\n${BLUE}[3/3] Assinando certificado do servidor com a CA Intermediária...${NC}"
openssl ca -config openssl-ca-intermediate.cnf \
    -extensions server_cert \
    -days 365 -notext -md sha256 \
    -in ca-intermediate/csr/server.csr \
    -out ca-intermediate/certs/server.crt
echo -e "${GREEN}✓ Certificado do servidor assinado (válido por 1 ano)${NC}"

echo -e "\n${GREEN}========================================"
echo "Certificado do servidor criado!"
echo "========================================${NC}"
echo ""
echo "Arquivos do servidor:"
echo "  - Chave privada: ca-intermediate/private/server.key"
echo "  - Certificado: ca-intermediate/certs/server.crt"
echo ""
