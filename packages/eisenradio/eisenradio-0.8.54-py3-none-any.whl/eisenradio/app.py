from eisenradio import wsgi
from waitress import serve

app = wsgi.app

print('\nPython WSGI server "Waitress" serves your requests ...\n')
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5050)
