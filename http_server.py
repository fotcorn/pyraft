from http import server
import json

class RequestHandler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        content = self.rfile.read(length)
        data = json.loads(content.decode('utf-8'))

        response = json.dumps(data).encode('utf-8')

        self.send_response(server.HTTPStatus.OK)
        self.send_header("Content-type", 'application/json')
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

if __name__ == '__main__':
    http_server = server.HTTPServer(('', 8000), RequestHandler)
    http_server.serve_forever()
