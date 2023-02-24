from server.utils import RoutingError, HTTP404


paths = {}


def route(suffix: str, viewset):
    if '/' in suffix:
        raise RoutingError()

    paths.update({suffix: viewset.list_create})
    paths.update({f'{suffix}/pk': viewset.retrieve_update_delete})


def appeal(uri: str, method: str, data: list, pk: int):
    if view := paths.get(uri):
        return view(method, data, pk)
    else:
        raise HTTP404


def direct(uri: str, method: str, data: list):
    if uri == '/':
        return appeal(uri, method, data, None)
    
    if uri[-1] == '/':
        uri = uri[1:-1].split('/')
    else:
        uri = uri[1:].split('/')
        
    if '' in uri or len(uri) > 2:
        raise HTTP404

    try:
        pk = int(uri[1])
    except IndexError:
        return appeal(uri[0], method, data, None)
    except ValueError:
        raise HTTP404
    else:
        return appeal(f'{uri[0]}/pk', method, data, pk)
