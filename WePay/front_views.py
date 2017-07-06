from django.core.handlers.wsgi import WSGIRequest

from base.response import response


def try_request(request):
    print(request.read().decode())
    return response(body=request.method)
