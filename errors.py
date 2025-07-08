from aiohttp import web

class HTTPError(web.HTTPException):
    def __init__(self, status_code: int, message: str | dict |list):
        self.status_code = status_code
        self.message = message
        

