FROM python:3.11-slim

WORKDIR /app

# requirements.txtに頼らず直接インストールする
RUN pip install fastapi uvicorn anthropic python-dotenv

COPY . .
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]