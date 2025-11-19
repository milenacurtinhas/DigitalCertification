# <center> Relatório do Trabalho T1 </center>
## <center>  Segurança em Computação – 2025/2 
## <center> Infraestrutura de Certificação Digital: Let's Encrypt e PKI Própria

---

### Informações do Grupo
- **Disciplina:** Segurança em Computação 2025/2
- **Integrantes:**  
  - Nome: Marcela Carpenter da Paixao   
  - Nome: Milena Curtinhas Santos

---

## 1. Arquitetura do Ambiente
Descreva e desenhe (use figuras) a arquitetura geral dos dois cenários implementados, destacando suas diferenças principais:

- **Cenário 1:** HTTPS com Certificado Válido via CA Privada (Root + Intermediária) usando Python.  

    Nesse cenário, toda a cadeia PKI (CA Raiz, CA Intermediária e certificados de servidor) é gerada e gerenciada programaticamente usando scripts em Python, utilizando principalmente a bibliotecas cryptography. A arquitetura consiste em módulos Python que criam as chaves privadas, geram as requisições de assinatura (CSR), assinam certificados e armazenam os arquivos em diretórios organizados. A configuração do servidor web HTTPS (exemplo Nginx) usa esses certificados gerados dinamicamente. Esse método enfatiza automação, flexibilidade e integração programática, permitindo personalização e extensão no processo de criação e renovação dos certificados conforme necessário, além de favorecer o aprendizado detalhado da estrutura e operações internas da PKI.

- **Cenário 2:** HTTPS com Certificado Válido via CA Privada (Root + Intermediária) usando OpenSSL.

    Neste cenário, a arquitetura baseia-se em comandos OpenSSL no terminal para gerar manualmente cada componente da PKI: a CA Raiz, a CA Intermediária, os certificados do servidor, gerando arquivos PEM e CRT que são utilizados na configuração do servidor HTTPS. A organização dos certificados e chaves é feita em diretórios fixos e o processo é menos automatizado, demandando a execução sequencial de comandos e scripts shell, ou manuais. Essa abordagem é altamente transparente, com controle direto sobre cada comando e parâmetro de certificação, sendo ideal para entender o funcionamento das ferramentas padrão de criptografia de certificados, mas com menos flexibilidade programática direta.

---

## 2. Tarefa 1 – HTTPS com Certificado Válido via CA Privada (Root + Intermediária) usando Python

### 2.1. Preparação do Ambiente
- Sistema operacional: Linux - Ubuntu  
- Ferramentas utilizadas: 

    Docker para criar os containers que encapsulam o servidor Nginx; Docker Compose para gerenciar, build e execução do container; Nginx como o servidor web usado dentro do container, configurado para usar os certificados TLS gerados pela sua PKI privada; Python com bibliotecas de criptografia para criação das CAs, geração e assinatura dos certificados por meio de Scripts Python, além do uso de PyOpenSSL para validação da cadeia de certificação via script Python; VSCode para editar Dockerfile, nginx.conf, docker-compose.yml e scripts Python.
  
- Versão do Docker / Nginx: Docker version 28.4.0, nginx version: nginx/1.29.3  
- Descreva e disponibilize a configuração do servidor web e a página de exemplo criada:

    A configuração do servidor web está no arquivo `tarefa1/nginx.conf`, que define um servidor HTTPS escutando na porta 443 para o domínio localhost, usando o certificado TLS localizado em `/etc/nginx/ssl/server_fullchain.crt` e a chave privada em `/etc/nginx/ssl/server_key.key`. O servidor Nginx serve arquivos estáticos do diretório `/usr/share/nginx/html`, cujo conteúdo corresponde à pasta html/ do projeto, incluindo a página inicial `index.html`. Essa página de exemplo é um arquivo HTML básico que demonstra a página que os usuários verão ao acessar o servidor via HTTPS, garantindo que a conexão está protegida e autenticada pelo certificado emitido pela sua infraestrutura PKI.

### 2.2. Emissão do Certificado
- Caminho do certificado gerado: tarefa1/ca_storage/server/server_cert.crt  
- Explique o processo de validação e emissão e quais arquivos foram gerados.

    Primeiramente, a CA Raiz autoassinada gera a chave privada e o certificado raiz (arquivo `ca_storage/root/root_cert.pem e chave root_key.key`), que serve como a autoridade confiável máxima; em seguida, a CA Intermediária tem sua própria chave e certificado (`ca_storage/intermediate/intermediate_cert.pem` e `intermediate_key.key`), que é assinado pela CA Raiz, formando uma cadeia de confiança; com essa cadeia, é gerada uma requisição de assinatura de certificado (CSR) para o servidor (`ca_storage/server/csr.csr`), que é então assinada pela CA Intermediária para criar o certificado do servidor (`ca_storage/server/server_cert.crt`), que junto à chave privada do servidor (`server_key.key`) será usado para o HTTPS; além disso, o arquivo `server_fullchain.crt` é gerado concatenando o certificado do servidor e o certificado da CA Intermediária, permitindo que servidores como o Nginx apresentem a cadeia completa para validadores externos. Para validar essa cadeia, é possível usar o script Python `validate_chain.py` que carrega esses certificados e verifica a validade e integridade da cadeia, garantindo que o certificado do servidor é confiável a partir da CA Raiz.

### 2.3. Configuração HTTPS no Nginx
- Descreva como foi feita a configuração do servidor para uso do certificado emitido.

    A configuração do servidor foi realizada configurando o Nginx em um container Docker para servir HTTPS utilizando os certificados gerados pela infraestrutura PKI criada em Python, onde o arquivo `server-fullchain.pem` contém a cadeia completa de certificados (servidor, intermediária, raiz) e a chave privada do servidor está no arquivo `server_key.key`; estes arquivos foram montados como volumes no container Nginx e referenciados na configuração do Nginx para ativar a camada de segurança SSL, enquanto a porta 8443 foi exposta para acesso externo, e para que os navegadores confiem na conexão segura, é necessário importar o certificado da CA raiz manualmente no navegador, garantindo assim uma comunicação segura e validada pela cadeia de certificação criada.

### 2.4. Resultados e Validação
- URL de acesso: https://localhost:8443/  
- Screenshot da página HTTPS: 

    <img src="tarefa1/screenshots/img1.png" width="1000">

- Resultado do comando de verificação: 

    Assinatura OK: <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=localhost)> assinado por <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=Intermediate CA)>

    Assinatura OK: <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=Intermediate CA)> assinado por <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=Root CA)>

    Assinatura OK: <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=Root CA)> assinado por <Name(C=BR,ST=Espirito Santo,L=Vitoria,O=Organização fictícia,CN=Root CA)>

    Cadeia de certificação completa: OK

- Screenshot do certificado no navegador (cadeado):

    <img src="tarefa1/screenshots/img2.png" width="1000">

---

## 3. Tarefa 2 – HTTPS com Certificado Válido via CA Privada (Root + Intermediária) usando OpenSSL

### 3.1. Criação da CA Raiz
- Explique o papel da CA raiz, descreva o processo de criação e a importância na cadeia de confiança.

    A CA Raiz é o ponto mais alto da cadeia de confiança em uma infraestrutura PKI, funcionando como a âncora de confiança para todos os certificados emitidos abaixo dela. O processo de criação da CA Raiz envolve a geração de um par de chaves criptográficas (pública e privada) e a emissão de um certificado autoassinado, que é um certificado firmado pela própria CA, pois não existe uma autoridade superior que a valide. A importância da CA Raiz está no fato de que todos os certificados intermediários e finais dependem da sua credibilidade para serem confiáveis; se a CA Raiz for confiável e segura, a cadeia inteira de certificação é considerada confiável. Como ela é autoassinada, seu certificado precisa estar presente e confiável nos dispositivos clientes (navegadores, sistemas operacionais) para validar corretamente os certificados da cadeia, garantindo comunicação segura e autenticada.

### 3.2. Criação da CA Intermediária
- Explique por que se utiliza uma CA intermediária, descrevendo o processo de criação e seus benefícios em relação à segurança.

    Uma CA intermediária é usada como um elo entre a CA raiz e os certificados finais emitidos aos usuários ou servidores, funcionando como uma extensão delegada da confiança da raiz; sua criação envolve a emissão de um certificado intermediário pela CA raiz, que passa a assinar e emitir certificados para as entidades finais, o que traz benefícios importantes para a segurança, como reduzir a exposição da CA raiz (que permanece offline ou restrita para maior proteção), permitir a segmentação e controle da emissão de certificados por diferentes áreas ou propósitos, além de aumentar a flexibilidade operacional da infraestrutura da PKI) tudo isso contribuindo para uma cadeia de confiança mais segura e gerenciável.

### 3.3. Emissão do Certificado do Servidor
- Caminho do `fullchain.crt`:  /tarefa2/ca-intermediate/certs/server-fullchain.pem  
- Descreva o processo de emissão do certificado do servidor e como ele foi assinado pela CA intermediária.

    O processo de emissão do certificado do servidor começa com a geração de uma chave privada e a criação de uma Solicitação de Assinatura de Certificado (CSR), que contém as informações do servidor, como o nome do domínio. Essa CSR é enviada para a CA intermediária, que utiliza sua chave privada para assinar digitalmente o certificado do servidor, validando sua autenticidade. A assinatura da CA intermediária cria uma ligação de confiança entre o certificado do servidor e a cadeia de certificação, que ligada à CA raiz. Esse processo permite que o certificado do servidor seja reconhecido como válido dentro da cadeia de confiança da PKI, já que a CA intermediária delega autoridade da CA raiz para emitir certificados aos servidores, aumentando a segurança ao manter a CA raiz protegida e usando as CA intermediárias para operações de emissão e revogação de certificados em ambientes controlados.

### 3.4. Importação da CA Raiz no Navegador
Descreva o procedimento adotado para importar o certificado raiz no navegador:  
- Caminho seguido no navegador: 

    Para importar o certificado no FireFox foi acessado o endereço: about:preferences#privacy -> na seção Certificados clique em Ver certificados -> na aba Autoridades, selecione Importar -> foi escolhido o arquivo de certificado da CA raiz (exemplo: ca-root/certs/ca-root.pem) -> e marcada a opção "Confiar nesta autoridade para identificar websites" para permitir que o navegador confie nos certificados emitidos por essa CA.
  
- Resultado esperado: navegador passou a confiar na CA criada? Justifique

    O navegador passou a confiar na CA criada porque o certificado da CA raiz foi manualmente importado e marcado como confiável nas configurações de certificados do navegador. Como consequência, todos os certificados emitidos pela CA intermediária validada por esta raiz passam a ser considerados confiáveis, evitando alertas de segurança e erros relacionados a certificados não confiáveis durante conexões HTTPS. Essa confiança manual é necessária para que uma PKI local ou privada funcione corretamente nos navegadores.

- Inclua uma captura de tela do certificado confiável. 

    <img src="tarefa2/screenshots/img7.png" width="1000">

### 3.5. Validação da Cadeia
- Resultado do comando de verificação: 

    Verificando certificado da CA Raiz...

            Subject: C = BR, ST = ES, L = Vitoria, O = UFES, OU = DI, CN = UFES Root CA, emailAddress = admin@ufes.br
    
            Subject Public Key Info:
    
                Public Key Algorithm: rsaEncryption

    Verificando certificado da CA Intermediária...

            Subject: C = BR, ST = ES, O = UFES, OU = DI, CN = UFES Intermediate CA, emailAddress = admin@ufes.br

            Subject Public Key Info:

                Public Key Algorithm: rsaEncryption

    Verificando certificado do servidor...

            Subject: C = BR, ST = ES, L = Vitoria, O = UFES, OU = DI, CN = localhost

            Subject Public Key Info:

                Public Key Algorithm: rsaEncryption



    Validando cadeia de certificação completa...

    ca-intermediate/certs/server.crt: OK

    Cadeia de certificação válida!

- Screenshot do navegador com HTTPS ativo e confiável: 

    <img src="tarefa2/screenshots/img2.png" width="1000">

---

## 4. Comparação entre os Dois Cenários
Responda às questões abaixo com base na experiência prática:

- Quais as principais diferenças entre o uso de Python e OpenSSL?

    O uso de Python para criação e gerenciamento de uma PKI privada é ideal pra maior automação, flexibilidade e integração programática, permitindo que todo o ciclo de vida dos certificados seja controlado por scripts de forma eficiente e escalável, enquanto o OpenSSL, sendo uma ferramenta de linha de comando, oferece controle direto e detalhado sobre cada aspecto da geração e assinatura dos certificados, sendo um processos manual que requer conhecimento técnico dos comandos, sendo ideal para operações pontuais e aprendizado dos fundamentos criptográficos.

- Em quais cenários cada abordagem é mais adequada?

    A abordagem com Python é mais adequada para cenários que demandam automação e reutilização, onde é necessário gerenciar dinamicamente a emissão, renovação e armazenamento de certificados em larga escala ou em ambientes que evoluem rapidamente. Já o uso do OpenSSL foca em transparência e controle das operações criptográficas sendo ideal para ambientes estáticos ou de configuração manual, onde o controle detalhado sobre cada comando e parâmetro é importante, casos em que a automação não é prioridade e o processo manual é suficiente.

- Por que a importação da CA raiz é necessária no segundo cenário?  

    A importação da CA raiz é necessária no cenário de PKI privada porque os certificados emitidos não são automaticamente reconhecidos como confiáveis pelos sistemas operacionais e navegadores, que têm pré-carregadas apenas as CAs públicas mais conhecidas. Sem importar manualmente a CA raiz privada, os clientes não conseguem validar a cadeia de confiança do certificado, resultando em alertas de segurança ou rejeição da conexão. Essa importação é o processo de informar aos dispositivos que a autoridade interna é legítima e confiável dentro daquele ambiente controlado, permitindo o uso seguro dos certificados gerados pela PKI própria.

---

## 5. Conclusões
- Apresente as principais lições aprendidas durante o projeto.  

    Foi possível aprender profundamente os conceitos fundamentais de criptografia assimétrica, estrutura e funcionamento de certificados digitais, controle e geração manual das CAs e certificados, além de entender a cadeia de confiança e como validar certificados em ambientes controlados. O uso das linguagens como Python ou o uso do OpenSSL permite automatizar processos complexos de criação, assinatura e gerenciamento dos certificados, desenvolvendo habilidades práticas em scripting e segurança de sistemas

- Explique a importância prática da certificação digital e da confiança em ambientes seguros.

    A certificação digital e a confiança em ambientes seguros são fundamentais para garantir a autenticidade, integridade e confidencialidade das comunicações digitais, protegendo usuários e sistemas contra fraudes, interceptações e ataques cibernéticos. Na prática, a certificação digital permite que as partes envolvidas confirmem a identidade umas das outras, estabelecendo uma cadeia de confiança que assegura que os dados não foram alterados durante a transmissão e que estão acessíveis apenas a destinatários autorizados. Isso é crucial para proteger transações financeiras, troca de informações sensíveis, acesso a sistemas corporativos e qualquer cenário onde a segurança da informação é prioritária, promovendo confiança e segurança em interações online.

---

## Checklist Final
| Item | Status |
|------|--------|
| Servidor Nginx funcional (Docker) | ✅ |
| Certificado Let's Encrypt emitido e válido | ✅ / ❌ |
| PKI própria criada (Root + Intermediária) | ✅ |
| Importação da CA raiz no navegador | ✅ |
| Cadeia de certificação validada com sucesso | ✅ |
| Relatório completo e entregue | ✅ |
| Apresentação prática (vídeo) | ✅ / ❌ |

---


