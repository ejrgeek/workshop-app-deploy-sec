import os
import subprocess
from datetime import datetime
from app import create_app

app = create_app()

def backup_db():
    with app.app_context():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.sql"
        
        cmd = [
            'pg_dump',
            '-h', 'localhost',
            '-U', 'app_user',
            '-d', 'empresa_db',
            '-f', backup_file,
            '-F', 'c'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = 'sua_senha'
        
        try:
            subprocess.run(cmd, env=env, check=True)
            app.logger.info(f"Backup criado: {backup_file}")
            return True
        except subprocess.CalledProcessError as e:
            app.logger.error(f"Falha no backup: {str(e)}")
            return False