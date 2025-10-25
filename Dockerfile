# Usa a imagem oficial do Python, otimizada para containers
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências primeiro para melhor cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação quando o container iniciar
CMD ["python", "app.py"]