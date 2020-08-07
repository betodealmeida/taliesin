from collections import defaultdict
from typing import Any
from typing import Callable

import jwt
from flask import abort
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response

WSGIApp = Callable[[Any, Any], Any]


class JWTAuth:
    def __init__(self, app: WSGIApp, secret: str):
        self.app = app
        self.secret = secret

    def __call__(self, environ, start_response):
        request = Request(environ)

        if "Authorization" not in request.headers or not request.headers[
            "Authorization"
        ].startswith("Bearer "):
            response = Response("Missing Authorization header", status=401)
            return response(environ, start_response)
        auth_token = request.headers["Authorization"].split(" ", 1)[1]

        try:
            payload = jwt.decode(auth_token, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            response = Response("Expired JWT", status=401)
            return response(environ, start_response)
        except jwt.InvalidTokenError:
            response = Response("Invalid JWT", status=401)
            return response(environ, start_response)

        # use defaultdict to store allowed methods for a given path
        allowed = defaultdict(list)
        allowed.update(payload.get("allowed", {}))
        allowed_methods = allowed[request.path]

        # are the path and method allowed?
        if request.method not in allowed_methods:
            response = Response("Path/method not allowed", status=403)
            return response(environ, start_response)

        return self.app(environ, start_response)
