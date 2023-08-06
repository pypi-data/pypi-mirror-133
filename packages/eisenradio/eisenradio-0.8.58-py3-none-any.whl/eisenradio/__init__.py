from os import path, environ
from flask import Flask
from eisenradio.instance.config_apfac import write_config, remove_config
from .api import api
script_path = path.dirname(__file__)


""" Flask application factory with blueprints  """

""" 'Home' and 'Util' load modules, templates, styles, favicon from its own project folders """


def create_app(test=None):    # must be None

    app = Flask(__name__,
                instance_path=path.join(script_path, 'instance'))

    with app.app_context():

        api.init_app(app)

        if test is not None:
            """------------- TEST RUN -------------------
            have to exec  write_config('test') at first from pytest! for init flask env
            not hard coding the path in config.py because of deploying the package elsewhere"""
            write_config('test')
            # remove in teardown

        if not test:
            # environ['WERKZEUG_RUN_MAIN'] = 'true'
            is_snap_device = 'SNAP' in environ  # write in [SNAP_USER_COMMON]

            if not is_snap_device:
                """------------- PROD -------------------"""
                write_config('prod')
                remove_config()
            if is_snap_device:
                """------------- SNAP -------------------"""
                write_config('snap')
                remove_config(environ["SNAP_USER_COMMON"])

        # helper stuff
        from eisenradio.lib.platform_helper import main as start_frontend
        from eisenradio.lib.eisdb import install_new_db as create_install_db
        # Import parts of the application, separated by routes
        from eisenradio.eisenhome import routes as home_routes
        from eisenradio.eisenutil import routes as util_routes

        # Register Blueprints (pointer to parts of the application, subprojects in production)
        app.register_blueprint(home_routes.eisenhome_bp)
        app.register_blueprint(util_routes.eisenutil_bp)

        create_install_db(app.config['DATABASE'])
        if test:
            print(f"\tapp.config:       {app.config}\n")
        if not test:
            start_frontend()
        return app

