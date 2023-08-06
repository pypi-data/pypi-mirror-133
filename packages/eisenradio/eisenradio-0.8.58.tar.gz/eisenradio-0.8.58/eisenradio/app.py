from logging import getLogger
from eisenradio import wsgi
from waitress import serve

logger = getLogger('waitress')
logger.setLevel("ERROR")


app = wsgi.app
print('\n Python WSGI server "Waitress" \n')
if __name__ == "__main__":
    serve(app, host='localhost', port=5050)
