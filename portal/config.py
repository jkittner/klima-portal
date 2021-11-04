import os


class Config:
    DB_PATH = os.environ.get('DATABASE_PATH') or 'app.db'
