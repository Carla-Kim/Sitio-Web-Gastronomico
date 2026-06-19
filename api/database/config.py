import os

SECRET_KEY = os.getenv('SECRET_KEY', 'gastronomico-ids-2026')
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')            
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

DB_NAME = os.getenv('DB_NAME', 'gestion_db')
DB_PORT = int(os.getenv('DB_PORT', 3306))

DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'port': DB_PORT,
    'charset': 'utf8mb4'
}
DB_NAME = "gastronomia_db"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "productos")