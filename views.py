from http.server import SimpleHTTPRequestHandler
import json
from models import Establishment

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/establishments':
            self._set_headers()
            establishments = Establishment.get_all()
            self.wfile.write(json.dumps([e.__dict__ for e in establishments]).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/establishments':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                establishment_data = json.loads(post_data)
                new_establishment = Establishment(**establishment_data)
                Establishment.add(new_establishment)
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Establishment added successfully"}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(405)
            self.end_headers()

    def do_PUT(self):
        if self.path == '/api/establishments':
            try:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                establishment_data = json.loads(put_data)
                Establishment.update(establishment_data)
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Establishment updated successfully"}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(405)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/api/establishments/'):
            try:
                ruc = self.path.split('/')[-1]
                Establishment.delete_by_ruc(ruc)
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Establishment deleted successfully"}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(405)
            self.end_headers()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
