from eisenradio import wsgi
from waitress import serve

app = wsgi.app

print('\n Python WSGI server pretty "Waitress" serves your requests ...\n')
if __name__ == "__main__":
    # serve(app, host='0.0.0.0', port=5050) in out on all ips, NEVER at home!!!, localhost is local internal loopback
    serve(app, host='localhost', port=5050)
