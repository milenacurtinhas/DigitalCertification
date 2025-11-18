# Tarefa 2 - PKI com Python

Implementação de uma Infraestrutura de Chaves Públicas (PKI) completa usando Python.

## Estrutura da PKI

- **CA Raiz (Root CA)**: Autoridade certificadora autoassinada
- **CA Intermediária**: Assinada pela CA Raiz
- **Certificado do Servidor**: Assinado pela CA Intermediária para `localhost`

## Execução Passo a Passo

### 1. Instalar dependências Python

```
python3 -m pip install -r requirements.txt
```

### 2. Gerar Certificado do Servidor

```
python main.py
```

Este script irá gerar a CA Raiz, CA Intermediária e o certificado do servidor.

### 3. Gerar cadeia completa para Nginx

```
cat ca_storage/server/server_cert.crt ca_storage/intermediate/intermediate_cert.pem > ca_storage/server/server_fullchain.crt
```

Esse comando irá concatenar o certificado do servidor com o certificado da CA Intermediária para formar a cadeia completa usada pelo Nginx

### 4. Build e deploy da imagem Docker

```
docker-compose build
docker-compose up -d
```

Esses comandos irão construir a imagem Docker com Nginx usando os certificados e rodar o container.

### 5. Importar CA Raiz no Navegador

#### Firefox:
1. Acesse `about:preferences#privacy`
2. "Certificados" → "Ver certificados"
3. Aba "Autoridades" → Importar
4. Selecione `ca_storage/root/root_cert.pem`

### 6. Acessar o Site:

Abra o navegador e acesse: `https://localhost:8443`

Você deverá ver o cadeado indicando conexão segura!

### 7. Verificar Cadeia de Certificação

```
python validate_chain.py > resultado_validacao.txt 2>&1
```

Saída esperada: `Cadeia de certificação: OK`

## Verificação dos certificados

### Saída do terminal

Ver aquivo `resultado_validacao.txt` para evidências da implementação funcionando.

### Screenshots

Ver pasta `screenshots/` para evidências visuais da implementação funcionando.

## Estrutura de Arquivos

```
tarefa1/
├── ca_manager.py
├── ca_storage
│   ├── intermediate
│   │   ├── intermediate_cert.pem
│   │   └── intermediate_key.key
│   ├── root
│   │   ├── root_cert.pem
│   │   └── root_key.key
│   └── server
│       ├── csr.csr
│       ├── server_cert.crt
│       ├── server_fullchain.crt
│       └── server_key.key
├── docker-compose.yml
├── Dockerfile
├── files_manager.py
├── html
│   └── index.html
├── main.py
├── nginx.conf
├── README.md
├── requirements.txt
├── screenshots
│   ├── img10.png
│   ├── img11.png
│   ├── img1.png
│   ├── img2.png
│   ├── img3.png
│   ├── img4.png
│   ├── img5.png
│   ├── img6.png
│   ├── img7.png
│   ├── img8.png
│   └── img9.png
├── validate_chain.py
```