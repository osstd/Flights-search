import os


class Config:
    SECRET_KEY = os.environ.get('F_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    TEQUILA_ENDPOINT = os.environ.get('T_E')
    TEQUILA_API_KEY = os.environ.get('T_KEY')
