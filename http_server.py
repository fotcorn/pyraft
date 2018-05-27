from http import server
import json


class RequestHandler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        content = self.rfile.read(length)
        data = json.loads(content.decode('utf-8'))

        self.server.handler(data)

        response = json.dumps({'status': 'ok'}).encode('utf-8')

        self.send_response(server.HTTPStatus.OK)
        self.send_header("Content-type", 'application/json')
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)


def serve_forever(handler, port):
    http_server = server.HTTPServer(('', port), RequestHandler)
    http_server.handler = handler
    http_server.serve_forever()
