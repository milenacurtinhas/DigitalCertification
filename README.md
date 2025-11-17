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

- **Cenário 1:** Let's Encrypt + ngrok — uso de uma autoridade certificadora pública para emissão automática de certificados válidos por meio do protocolo ACME.  
- **Cenário 2:** PKI própria (Root + Intermediária) — criação e operação de uma infraestrutura de chaves públicas local, com emissão de certificados assinados por uma CA interna.

---

## 2. Tarefa 1 – HTTPS com Certificado Público (Let's Encrypt + ngrok)

### 2.1. Preparação do Ambiente
- Sistema operacional: ____________________  
- Ferramentas utilizadas: ____________________  
- Versão do Docker / Nginx: Docker version 28.4.0, nginx version: nginx/1.29.3  
- Descreva e disponibilize a configuração do servidor web e a página de exemplo criada:
A configuração do servidor web está no arquivo tarefa1/nginx.conf, que define um servidor HTTPS escutando na porta 443 para o domínio localhost, usando o certificado TLS localizado em /etc/nginx/ssl/server.crt e a chave privada em /etc/nginx/ssl/server_key.key. O servidor Nginx serve arquivos estáticos do diretório /usr/share/nginx/html, cujo conteúdo corresponde à pasta html/ do seu projeto, incluindo a página inicial index.html. Essa página de exemplo é um arquivo HTML básico que demonstra a página que os usuários verão ao acessar o servidor via HTTPS, garantindo que a conexão está protegida e autenticada pelo certificado emitido pela sua infraestrutura PKI.

### 2.2. Exposição com ngrok
- Domínio público gerado: ______________________________  
- Explique como o túnel foi utilizado para permitir a validação do domínio pelo Let's Encrypt.

### 2.3. Emissão do Certificado
- Caminho do certificado gerado: _________________________  
- Explique o processo de validação e emissão e quais arquivos foram gerados.

### 2.4. Configuração HTTPS no Nginx
- Descreva como foi feita a configuração do servidor para uso do certificado emitido.
A configuração do servidor foi realizada configurando o Nginx em um container Docker para servir HTTPS utilizando os certificados gerados pela infraestrutura PKI criada em Python, onde o arquivo `server-fullchain.pem` contém a cadeia completa de certificados (servidor, intermediária, raiz) e a chave privada do servidor está no arquivo `server_key.key`; estes arquivos foram montados como volumes no container Nginx e referenciados na configuração do Nginx para ativar a camada de segurança SSL, enquanto a porta 8443 foi exposta para acesso externo, e para que os navegadores confiem na conexão segura, é necessário importar o certificado da CA raiz manualmente no navegador, garantindo assim uma comunicação segura e validada pela cadeia de certificação criada.

### 2.5. Resultados e Validação
- URL de acesso: https://localhost:8443/  
- Screenshot da página HTTPS: ![pag https](tarefa1/screenshots/img1.png)
- Resultado do comando de verificação: Certificado 0 verificado com sucesso pelo emissor 1

    Certificado 1 verificado com sucesso pelo emissor 2

    Certificado raiz é autoassinado e válido.

    Validação da cadeia de certificação foi bem-sucedida! 
- Screenshot do certificado no navegador (cadeado): ![cert1](tarefa1/screenshots/img2.png)

---

## 3. Tarefa 2 – HTTPS com PKI Própria (Root + Intermediária)

### 3.1. Criação da CA Raiz
- Explique o papel da CA raiz, descreva o processo de criação e a importância na cadeia de confiança.

### 3.2. Criação da CA Intermediária
- Explique por que se utiliza uma CA intermediária, descrevendo o processo de criação e seus benefícios em relação à segurança.

### 3.3. Emissão do Certificado do Servidor
- Caminho do `fullchain.crt`: ____________________________  
- Descreva o processo de emissão do certificado do servidor e como ele foi assinado pela CA intermediária.

### 3.4. Importação da CA Raiz no Navegador
Descreva o procedimento adotado para importar o certificado raiz no navegador:  
- Caminho seguido no navegador: __________________________  
- Resultado esperado: navegador passou a confiar na CA criada? Justifique
- Inclua uma captura de tela do certificado confiável.

### 3.5. Validação da Cadeia
- Resultado do comando de verificação: ____________________________  
- Screenshot do navegador com HTTPS ativo e confiável: *(inserir imagem)*

---

## 4. Comparação entre os Dois Cenários
Responda às questões abaixo com base na experiência prática:

- Quais as principais diferenças entre o uso de certificados públicos e privados?  
- Em quais cenários cada abordagem é mais adequada?  
- Por que a importação da CA raiz é necessária no segundo cenário?  

---

## 5. Conclusões
- Apresente as principais lições aprendidas durante o projeto.  
- Explique a importância prática da certificação digital e da confiança em ambientes seguros.

---

## Checklist Final
| Item | Status |
|------|--------|
| Servidor Nginx funcional (Docker) | ✅ / ❌ |
| Certificado Let's Encrypt emitido e válido | ✅ / ❌ |
| PKI própria criada (Root + Intermediária) | ✅ / ❌ |
| Importação da CA raiz no navegador | ✅ / ❌ |
| Cadeia de certificação validada com sucesso | ✅ / ❌ |
| Relatório completo e entregue | ✅ / ❌ |
| Apresentação prática (vídeo) | ✅ / ❌ |

---


