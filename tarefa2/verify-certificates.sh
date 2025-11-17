#!/bin/bash

echo "========================================"
echo "Verificando Cadeia de Certificação"
echo "========================================"


echo -e "\nVerificando certificado da CA Raiz..."
openssl x509 -noout -text -in ca-root/certs/ca-root.pem | grep -A 2 "Subject:"

echo -e "\nVerificando certificado da CA Intermediária..."
openssl x509 -noout -text -in ca-intermediate/certs/ca-intermediate.pem | grep -A 2 "Subject:"

echo -e "\nVerificando certificado do servidor..."
openssl x509 -noout -text -in ca-intermediate/certs/server.crt | grep -A 2 "Subject:"

echo -e "\nValidando cadeia de certificação completa..."
openssl verify -CAfile ca-root/certs/ca-root.pem \
    -untrusted ca-intermediate/certs/ca-intermediate.pem \
    ca-intermediate/certs/server.crt

if [ $? -eq 0 ]; then
    echo -e "Cadeia de certificação válida!"
else
    echo -e " Erro na validação da cadeia"
    exit 1
fi

echo -e "\n========================================"
echo "Verificação concluída com sucesso!"
echo "========================================"