# Projeto de apresentação do Workshop de Deploy e Segurança


## Pré-requisitos

- Debian/Ubuntu Linux
- Python 3.x
- PostgreSQL
- Git

## Instalação
Este projeto consiste em uma aplicação Flask integrada com PostgreSQL. Abaixo estão as instruções para configurar o ambiente de desenvolvimento e produção.

### 1. Instalação de Pacotes

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar dependências do Python
sudo apt install -y python3-dev python3-pip virtualenv

sudo apt install -y postgresql postgresql-contrib

```

### 2. Configuração do SSH (opcional)

```bash
sudo nano etc/ssh/sshd_config
# alterar -> PermitRootLogin yes
sudo systemctl restart ssh
```

### 3. Configuração do Banco de Dados

```bash
# iniciar serviço do banco
sudo systemctl start postgresql
sudo systemctl status postgresql
```

```bash
# Configuração e criação de tabelas
sudo -u postgres psql

CREATE USER app_user WITH PASSWORD 'SENHA-APP-EMPRESA';

CREATE DATABASE empresa_db WITH OWNER app_user;

\c empresa_db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

GRANT ALL PRIVILEGES ON DATABASE empresa_db TO app_user;

ALTER USER app_user CREATEDB;

\q
```

### 4. Configurando Aplicação
```bash
virtualenv venv

. /venv/bin/activate

pip3 install -r requirements.txt
```

### 5. Iniciando Aplicação
```bash
# Inicialize o sistema de migração
flask db init

# Crie a primeira migração (irá gerar os schemas auth e hr)
flask db migrate -m "Initial PostgreSQL setup"

# Aplique as migrações
flask db upgrade
```

### 6. NUNCA JAMAIS DEVE SER FEITO NO MUNDO REAL
```bash
python create_first_user.py
```

### 7. Executando a aplicação
```bash
flask --app app run --debug --host=0.0.0.0
```