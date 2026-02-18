# FROM: tecnologia que será a base de criação da imagem.
# WORKDIR: diretório da imagem na qual os comandos serão executados.
# COPY: comando para copiar o código fonte para a imagem.
# RUN: comando para instalação de dependências.
# CMD: comando para executar o seu código quando o container for criado.

# Imagem base derivada do Node
FROM node

# Diretório de trabalho
WORKDIR /app

# Comando para copiar os arquivos para a pasta /app da imagem
COPY . /app

# Comando para instalar as dependências
RUN npm install

# Comando para inicializar (executar) a aplicação
CMD ["node", "/app/services/shipping/index.js"]