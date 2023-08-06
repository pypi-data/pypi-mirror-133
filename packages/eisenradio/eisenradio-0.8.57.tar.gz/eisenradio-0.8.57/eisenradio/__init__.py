from os import path, makedirs
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
            have to write_config('test') at first from pytest! for init flask env.   ???"""
            write_config('test')
            # remove in teardown

        if not test:
            """------------- PROD -------------------"""
            write_config('prod')
            remove_config()

        # helper stuff
        from eisenradio.lib.platform_helper import main as start_frontend
        from eisenradio.lib.eisdb import install_new_db as create_install_db
        # Import parts of the application, separated by routes
        from eisenradio.eisenhome import routes as home_routes
        from eisenradio.eisenutil import routes as util_routes

        # Register Blueprints (pointer to parts of the application, subprojects in production)
        app.register_blueprint(home_routes.eisenhome_bp)
        app.register_blueprint(util_routes.eisenutil_bp)

        if test:
            print(f"\tapp.config:       {app.config}\n")
            create_install_db(app.config['DATABASE'])
        if not test:
            create_install_db(app.config['DATABASE'])
            start_frontend()

        return app

