from http import server
import json
import threading

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

        print('resetting timer')
        start_timer()

        self.wfile.write(response)


def start_timer():
    if start_timer.timer:
        start_timer.timer.cancel()
    start_timer.timer = threading.Timer(1, timeout_task)
    start_timer.timer.start()
start_timer.timer = None


def timeout_task():
    print('timeout!')
    start_timer()


if __name__ == '__main__':
    start_timer()

    http_server = server.HTTPServer(('', 8000), RequestHandler)
    http_server.serve_forever()
