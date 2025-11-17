# Tarefa 2 - PKI com OpenSSL

Implementação de uma Infraestrutura de Chaves Públicas (PKI) completa usando OpenSSL.

## Estrutura da PKI

- **CA Raiz (Root CA)**: Autoridade certificadora autoassinada
- **CA Intermediária**: Assinada pela CA Raiz
- **Certificado do Servidor**: Assinado pela CA Intermediária para `localhost`

## Pré-requisitos

- Docker e Docker Compose instalados
- OpenSSL instalado
- Navegador web

## Execução Passo a Passo

### 1. Criar a Infraestrutura de CA

```
./setup-ca.sh
```

Este script irá:
- Criar CA Raiz com chave RSA 4096 bits
- Gerar certificado autoassinado da CA Raiz (válido por 10 anos)
- Criar CA Intermediária com chave RSA 4096 bits
- Assinar certificado da CA Intermediária com a CA Raiz (válido por 5 anos)
- Criar bundle da cadeia de certificação

### 2. Gerar Certificado do Servidor

```
./generate-server-cert.sh
```

Este script irá:
- Gerar chave privada do servidor (RSA 2048 bits)
- Criar Certificate Signing Request (CSR)
- Assinar certificado com a CA Intermediária (válido por 1 ano)

### 3. Iniciar Servidor Nginx

```
docker-compose up -d
```

### 4. Importar CA Raiz no Navegador

#### Firefox:
1. Acesse `about:preferences#privacy`
2. "Certificados" → "Ver certificados"
3. Aba "Autoridades" → Importar
4. Selecione `ca-root/certs/ca-root.pem`

### 5. Acessar o Site:

Abra o navegador e acesse: `https://localhost`

Você deverá ver o cadeado indicando conexão segura!

### 6. Verificar Cadeia de Certificação

```
./verify-certificates.sh > resultado_validacao.txt 2>&1
```

Saída esperada: `ca-intermediate/certs/server.crt: OK`

#### Validar a cadeia de certificação no terminal:

```
openssl verify -CAfile ca-root/certs/ca-root.pem \
    -untrusted ca-intermediate/certs/ca-intermediate.pem \
    ca-intermediate/certs/server.crt

```

## Verificação dos certificados

### Saída do terminal

Ver aquivo `resultado_validacao.txt` para evidências da implementação funcionando.

### Screenshots

Ver pasta `screenshots/` para evidências visuais da implementação funcionando.

## Estrutura de Arquivos

```
tarefa2/
├── ca-intermediate
│   ├── certs
│   │   ├── ca-chain.pem
│   │   ├── ca-intermediate.pem
│   │   ├── server.crt
│   │   └── server-fullchain.pem
│   ├── crl
│   ├── csr
│   │   ├── ca-intermediate.csr
│   │   └── server.csr
│   ├── index.txt
│   ├── index.txt.attr
│   ├── index.txt.old
│   ├── newcerts
│   │   └── 1000.pem
│   ├── private
│   │   ├── ca-intermediate.key
│   │   └── server.key
│   ├── serial
│   └── serial.old
├── ca-root
│   ├── certs
│   │   └── ca-root.pem
│   ├── crl
│   ├── index.txt
│   ├── index.txt.attr
│   ├── index.txt.old
│   ├── newcerts
│   │   └── 1000.pem
│   ├── private
│   │   └── ca-root.key
│   ├── serial
│   └── serial.old
├── docker-compose.yml
├── generate-server-cert.sh
├── html
│   └── index.html
├── nginx.conf
├── openssl-ca-intermediate.cnf
├── openssl-ca-root.cnf
├── README.md
├── resultado_validacao.txt
├── screenshots
│   ├── img10.png
│   ├── img1.png
│   ├── img2.png
│   ├── img3.png
│   ├── img4.png
│   ├── img5.png
│   ├── img6.png
│   ├── img7.png
│   ├── img8.png
│   └── img9.png
├── setup-ca.sh
└── verify-certificates.sh
```