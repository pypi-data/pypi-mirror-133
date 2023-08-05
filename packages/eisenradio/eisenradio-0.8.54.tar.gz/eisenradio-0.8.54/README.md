Web radio expandable collection
---
 * organize your web radios, delete and update 
 * upload your favorite pictures and comments to the local database
 * this guy is a web server application using the flask framework (blueprints and app factory)
 * Android: download to mobile, rename *WHL to *ZIP, extract with file manager
 * https://pypi.org/project/eisenradio-apk/ , uses Python Kivy library for multi-touch on start-up `https://pypi.org/project/Kivy/#files`
 * Linux SNAP user find uninstall information at the bottom 
 
pip install
-
	""" xxs Linux xxs """
    $ pip3 install eisenradio
    $ python3 -m eisenradio.wsgi  # watch flask

    """ xxm Windows xxm """
    > pip install eisenradio
    > python -m eisenradio.wsgi

    """ xxl big company xxl """
    $$$ pip3 install eisenradio
    $$$ python3 -m eisenradio.app  # serve flask
    """ for the sake of completeness, a python
        production server 'waitress' is started """
---
Pytest
---
> ~ ... /test/functional$ python3 -m pytest -s    # -s print to console

find the modified test db in ./app_writable/db

Uninstall
---
To completely delete all remnants of the module
find its location.

>$ pip3 show eisenradio

>$ pip3 uninstall eisenradio

Location: ... /python310/site-packages

SNAP user delete the database folder in their home; 
on startup shown in
[SNAP_USER_COMMON] 
>SNAP_USER_COMMON (your Database lives here, backup if you like): /home/osboxes/snap/eisenradio/common
