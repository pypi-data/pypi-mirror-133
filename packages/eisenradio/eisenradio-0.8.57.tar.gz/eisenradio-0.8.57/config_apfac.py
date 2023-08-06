from os import path, remove
from eisenradio.config import script_path

# SECRET_KEY
secret_key = 'SECRET_KEY=9fc2e5bd8372430fb6a1012af0b51f37'
# PRODUCTION, DEV
db_path_prod = path.join(script_path, 'app_writeable', 'db', 'database.db')
# TEST
db_path_test = path.join(script_path, 'app_writeable', 'db_test', 'eisenradio_test.db')

list_prod = [
        'FLASK_ENV=production',
        'DEBUG=False',
        'TESTING=False',
        'DATABASE=' + db_path_prod,
        secret_key
    ]

list_test = [
        'FLASK_ENV=development',
        'DEBUG=True',
        'TESTING=True',
        'DATABASE=' + db_path_test,
        secret_key
    ]

list_dev = [
        'FLASK_ENV=development',
        'DEBUG=True',
        'TESTING=True',
        'DATABASE=' + db_path_prod,
        secret_key
    ]


def load_config(conf=None):
    loader = ''
    if conf is None:
        conf = 'dev'
    if conf == 'prod':
        loader = list_prod
    if conf == 'test':
        loader = list_test
    if conf == 'dev':
        loader = list_dev
    print(path.join(script_path, '.env'))
    print(loader)
    with open(path.join(script_path, '.env'), 'w') as writer:
        for line in loader:
            writer.write(line + '\n')
        writer.flush()


def remove_config():
    remove(path.join(script_path, '.env'))
