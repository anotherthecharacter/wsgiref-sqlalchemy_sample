import json

from server.distributor import direct
from server.utils import HTTP404


def prepare(request, boundary):
    fields = {}

    while True:
        receive = request.readline().decode().strip()
    
        if receive == boundary:
            break

        if receive.startswith('Content-Disposition: form-data;'):
            key = receive[38:-1]
            request.readline()
            value = request.readline().decode().strip()
            fields.update({key: value})
        
    return fields


def app(environ, start_response):
    if environ['REQUEST_METHOD'] in ('POST', 'PUT', 'PATCH') and environ['CONTENT_TYPE'].startswith('multipart/form-data;') and environ['CONTENT_LENGTH'] != '0':
        boundary = '--' + environ['CONTENT_TYPE'][30:] + '--'
        data = prepare(environ['wsgi.input'], boundary)
    else:
        data = {}
    
    try:
        response = direct(environ['PATH_INFO'], environ['REQUEST_METHOD'], data)
        start_response(response[0], [('Content-Type','text/plain; charset=utf-8')])
        return [json.dumps(response[1]).encode('utf-8')]
    except HTTP404:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [json.dumps({'detail': 'Not found.'}).encode('utf-8')]
