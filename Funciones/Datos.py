# Configuración de la conexión a la base de datos
# Puedes modificar estos valores según tu configuración
import os
from dotenv import load_dotenv

load_dotenv()

Host = os.getenv("DB_HOST", "nioyfp.mysql.pythonanywhere-services.com")
User = os.getenv("DB_USER", "nioyfp")
Password = os.getenv("DB_PASSWORD", "jadelka_5677")
Database = os.getenv("DB_NAME", "nioyfp$ventas")
