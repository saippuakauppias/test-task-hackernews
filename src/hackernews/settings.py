SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'REQUIRED_SETTINGS': [
        'DB_TYPE',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME'
    ],
}

DB_TYPE = None
DB_USER = None
DB_PASSWORD = None
DB_HOST = None
DB_PORT = None
DB_NAME = None

DB_DSN = "{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
