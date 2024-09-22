# Usar uma imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar apenas os arquivos necessários para o servidor
COPY ./models/service/servidor_threads.py ./models/service/
COPY ./dados/ ./dados/
COPY ./ServerON.py ./
COPY ./requirements.txt ./

# Instalar as dependências
# RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o servidor vai usar (ajuste conforme sua configuração)
EXPOSE 65432

# Comando para iniciar o servidor
CMD ["python3", "./ServerON.py"]

