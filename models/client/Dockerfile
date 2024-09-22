# Usar uma imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar apenas os arquivos necessários para o cliente
COPY ./models/client/utils_cliente.py ./models/client/
COPY ./models/client/cliente_threads.py ./models/client/
COPY ./App_main.py ./
COPY ./requirements.txt ./

# Instalar as dependências
#RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo cliente, se necessário (ajuste conforme sua configuração)
EXPOSE 65433

# Comando para iniciar o cliente
CMD ["python3", "./App_main.py"]

