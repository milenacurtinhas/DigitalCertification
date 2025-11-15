#!/bin/bash

set -e

echo "========================================"
echo "Criando Infraestrutura de CA"
echo "========================================"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# PARTE 1: Criar CA Raiz
# ========================================

echo -e "\n${BLUE}[1/5] Criando estrutura de diretórios da CA Raiz...${NC}"
mkdir -p ca-root/{certs,crl,newcerts,private}
chmod 700 ca-root/private
echo 1000 > ca-root/serial
touch ca-root/index.txt
echo -e "${GREEN}✓ Estrutura da CA Raiz criada${NC}"

echo -e "\n${BLUE}[2/5] Gerando chave privada da CA Raiz (RSA 4096 bits)...${NC}"
openssl genrsa -aes256 -out ca-root/private/ca-root.key 4096
chmod 400 ca-root/private/ca-root.key
echo -e "${GREEN}✓ Chave privada da CA Raiz gerada${NC}"

echo -e "\n${BLUE}[3/5] Criando certificado autoassinado da CA Raiz...${NC}"
openssl req -config openssl-ca-root.cnf \
    -new -x509 -days 3650 \
    -key ca-root/private/ca-root.key \
    -sha256 -extensions v3_ca \
    -out ca-root/certs/ca-root.pem
echo -e "${GREEN}✓ Certificado da CA Raiz criado (válido por 10 anos)${NC}"

# ========================================
# PARTE 2: Criar CA Intermediária
# ========================================

echo -e "\n${BLUE}[4/5] Criando estrutura de diretórios da CA Intermediária...${NC}"
mkdir -p ca-intermediate/{certs,crl,csr,newcerts,private}
chmod 700 ca-intermediate/private
echo 1000 > ca-intermediate/serial
touch ca-intermediate/index.txt
echo -e "${GREEN}✓ Estrutura da CA Intermediária criada${NC}"

echo -e "\n${BLUE}[5/5] Gerando chave privada da CA Intermediária (RSA 4096 bits)...${NC}"
openssl genrsa -aes256 -out ca-intermediate/private/ca-intermediate.key 4096
chmod 400 ca-intermediate/private/ca-intermediate.key
echo -e "${GREEN}✓ Chave privada da CA Intermediária gerada${NC}"

echo -e "\n${BLUE}Criando CSR da CA Intermediária...${NC}"
openssl req -config openssl-ca-intermediate.cnf \
    -new -sha256 \
    -key ca-intermediate/private/ca-intermediate.key \
    -out ca-intermediate/csr/ca-intermediate.csr
echo -e "${GREEN}✓ CSR da CA Intermediária criado${NC}"

echo -e "\n${BLUE}Assinando certificado da CA Intermediária com a CA Raiz...${NC}"
openssl ca -config openssl-ca-root.cnf \
    -extensions v3_intermediate_ca \
    -days 1825 -notext -md sha256 \
    -in ca-intermediate/csr/ca-intermediate.csr \
    -out ca-intermediate/certs/ca-intermediate.pem
echo -e "${GREEN}✓ Certificado da CA Intermediária assinado (válido por 5 anos)${NC}"

echo -e "\n${BLUE}Criando bundle da cadeia de certificação...${NC}"
cat ca-intermediate/certs/ca-intermediate.pem \
    ca-root/certs/ca-root.pem > ca-intermediate/certs/ca-chain.pem
echo -e "${GREEN}✓ Cadeia de certificação criada${NC}"

echo -e "\n${GREEN}========================================"
echo "Infraestrutura de CA criada com sucesso!"
echo "========================================${NC}"
echo ""
echo "Arquivos importantes:"
echo "  - CA Raiz: ca-root/certs/ca-root.pem"
echo "  - CA Intermediária: ca-intermediate/certs/ca-intermediate.pem"
echo "  - Cadeia completa: ca-intermediate/certs/ca-chain.pem"
echo ""
