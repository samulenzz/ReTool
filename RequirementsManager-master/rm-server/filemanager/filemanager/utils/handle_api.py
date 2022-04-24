import json
from typing import Callable,List
from flask import request, Response
from functools import wraps

def handle_response(func:Callable):
    @wraps(func)
    def _func():
        resp=func()
        return Response(json.dumps(resp), mimetype='application/json')

    return _func