from aiohttp import web


class HttpServer(object):
    def __init__(self, handler_func):
        self.handler_func = handler_func

    async def handle(self, request: web.Request):
        data = await request.json()
        response = self.handler_func(data)
        return web.json_response(response)

    def run(self, port):
        app = web.Application()
        app.add_routes([web.post('/', self.handle)])
        web.run_app(app, port=port)
