import json

from server.distributor import direct


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
    if environ['REQUEST_METHOD'] in ('POST', 'PUT', 'PATCH'):
        if environ['CONTENT_TYPE'].startswith('multipart/form-data;') and environ['CONTENT_LENGTH'] != '0':
            boundary = '--' + environ['CONTENT_TYPE'][30:] + '--'
            data = prepare(environ['wsgi.input'], boundary)
        else:
            ...  # TODO: JSON handle
            ...  # TODO: Required fields by serializer
    else:
        ...  # TODO: NON_BODY_METHODS
    
    response = direct(environ['PATH_INFO'], environ['REQUEST_METHOD'], data)

    if response:
        start_response("200 OK", [('Content-Type','text/plain; charset=utf-8')])
        return [json.dumps(response).encode('utf-8')]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [''.encode('utf-8')]
