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

### 8. Usando Gunicorn para Produção
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

```bash
#script de inicialização automatica
echo 'cd /caminho/do/projeto && source venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:8000 app:app &' >> ~/.bashrc
```

### 9. Usando Gunicorn+Nginx

```bash
sudo nano /etc/systemd/system/flaskapp.service
```


Dentro do arquivo, colar:
```bash
[Unit]
Description=Projeto Workshop Flask
After=network.target

[Service]
User=usuario
Group=www-data
WorkingDirectory=/caminho/do/projeto
Environment="PATH=/caminho/do/projeto/venv/bin"
ExecStart=/caminho/do/projeto/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Ativando o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo systemctl status flaskapp
```

Instalando Nginx
```bash
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

Configurando Proxy Reverso
```bash
sudo nano /etc/nginx/sites-available/flaskapp
```

Dentro do arquivo:
```bash
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /caminho/do/projeto/static/;
        expires 30d;
    }
}
```


Permissões aos arquivos estáticos:
```bash
sudo chmod -R 755 /caminho/do/projeto/static
sudo chown -R www-data:www-data /caminho/do/projeto/static

```

Ativando serviço:
```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

Verificando logs:
```bash
sudo tail -50 /var/log/nginx/error.log
```

### 10. Tentando configurar HTTPS com Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d localhost
sudo certbot renew --dry-run
```


### 10. Montando Servidor WSGI Próprio
```bash
# EM BREVE
```
