from os import path, remove
from dotenv import load_dotenv

try:
    from flask import current_app
except ImportError:
    pass

this_script_dir = path.dirname(__file__)
# get root of app, rip off one subdir .go up
conf_path = path.dirname(this_script_dir)


def write_config(conf, empty_db=None):
    global this_script_dir
    radio_db_dir = path.join(conf_path, 'app_writeable', 'db')

    # SECRET_KEY
    secret_key = 'SECRET_KEY=9fc2e5bd8372430fb6a1012af0b51f37'
    secret_num = '9fc2e5bd8372430fb6a1012af0b51f37'
    # PRODUCTION, DEV
    db_path_prod = path.join(radio_db_dir, 'database.db')
    # TEST
    db_path_test = path.join(radio_db_dir, 'eisenradio_test.db')

    if empty_db is None:
        empty_db = 'False'
    if empty_db == 'True':
        empty_db = 'True'

    list_prod = [
        'DATABASE=' + db_path_prod,
        'FLASK_ENV=production',
        'DEBUG=False',
        'TESTING=False',
        secret_key,
        'EMPTY_DB=' + empty_db
    ]

    list_test = [
        'DATABASE=' + db_path_test,
        'FLASK_ENV=development',
        'DEBUG=True',
        'TESTING=True',
        secret_key,
        'EMPTY_DB=' + empty_db
    ]

    list_dev = [
        'DATABASE=' + db_path_prod,
        'FLASK_ENV=development',
        'DEBUG=True',
        'TESTING=True',
        secret_key,
        'EMPTY_DB=' + empty_db
    ]

    loader = ''
    db = ''
    f_env = ''
    debug = ''
    testing = ''

    if conf == 'prod':
        loader = list_prod
        db = db_path_prod
        f_env = 'production'
        debug = 'False'
        testing = 'False'
    if conf == 'test':
        loader = list_test
        db = db_path_test
        f_env = 'development'
        debug = 'True'
        testing = 'True'
    if conf == 'dev':
        loader = list_dev
        db = db_path_prod
        f_env = 'development'
        debug = 'True'
        testing = 'True'

    remove_config()
    with open(path.join(this_script_dir, '.env'), 'w') as writer:
        for line in loader:
            writer.write(line + '\n')
        writer.flush()

    load_config_os()

    try:
        current_app.config.update(SECRET_KEY=secret_num,
                                  DATABASE=path.abspath(db),
                                  FLASK_ENV=f_env,
                                  DEBUG=debug,
                                  TESTING=testing,
                                  )
    except RuntimeError:
        """test from outside can not connect to flask 'current_app' """
        pass


def load_config_os():
    global this_script_dir
    dotenv_loader = load_dotenv(path.join(this_script_dir, '.env'))


def remove_config():
    global this_script_dir
    try:
        remove(path.join(this_script_dir, '.env'))
    except OSError:
        pass
