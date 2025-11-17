FROM nginx:latest

# Cria diretório para os certificados no container
RUN mkdir -p /etc/nginx/ssl

# Copia os certificados do servidor e a chave para o container
COPY ca_storage/server/server_fullchain.crt /etc/nginx/ssl/server_fullchain.crt
COPY ca_storage/server/server_key.key /etc/nginx/ssl/server_key.key

# Copia o arquivo index.html da pasta html para a pasta padrão do Nginx
COPY html/index.html /usr/share/nginx/html/index.html

# Copia o arquivo de configuração nginx.conf para dentro do container
COPY nginx.conf /etc/nginx/conf.d/default.conf