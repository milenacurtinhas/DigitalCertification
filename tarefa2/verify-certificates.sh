#!/bin/bash

echo "========================================"
echo "Verificando Cadeia de Certificação"
echo "========================================"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${BLUE}Verificando certificado da CA Raiz...${NC}"
openssl x509 -noout -text -in ca-root/certs/ca-root.pem | grep -A 2 "Subject:"

echo -e "\n${BLUE}Verificando certificado da CA Intermediária...${NC}"
openssl x509 -noout -text -in ca-intermediate/certs/ca-intermediate.pem | grep -A 2 "Subject:"

echo -e "\n${BLUE}Verificando certificado do servidor...${NC}"
openssl x509 -noout -text -in ca-intermediate/certs/server.crt | grep -A 2 "Subject:"

echo -e "\n${BLUE}Validando cadeia de certificação completa...${NC}"
openssl verify -CAfile ca-root/certs/ca-root.pem \
    -untrusted ca-intermediate/certs/ca-intermediate.pem \
    ca-intermediate/certs/server.crt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cadeia de certificação válida!${NC}"
else
    echo -e "${RED}✗ Erro na validação da cadeia${NC}"
    exit 1
fi

echo -e "\n${GREEN}========================================"
echo "Verificação concluída com sucesso!"
echo "========================================${NC}"
