#coding: utf-8

"""
decorators 装饰器
"""
import json
from django.http import HttpResponse


def login_required_json(f):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            result = dict()
            result["success"] = False
            result["message"] = "The user is not authenticated"
            return HttpResponse(content=json.dumps(result),
                               mimetype="application/json")
        else:
            return f(request, *args, **kwargs)

    return inner