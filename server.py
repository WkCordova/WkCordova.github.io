from http.server import HTTPServer
from views import RequestHandler
from models import init_db
import os

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    # Crear la carpeta 'data' si no existe
    if not os.path.exists('data'):
        print("Creating 'data' directory.")
        os.makedirs('data')

    # Inicializar la base de datos
    init_db()

    # Cambiar al directorio estático para servir archivos estáticos
    os.chdir('static')
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
