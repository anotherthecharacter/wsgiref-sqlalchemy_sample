class RoutingError(Exception):

    def __str__(self) -> str:
        return 'An error occurred while routing the URLs. Perhaps you have inserted a slashes "/" into suffixes?'


paths = {}


def route(suffix: str, viewset):
    if '/' in suffix:
        raise RoutingError()

    paths.update({suffix: viewset.list_create})
    paths.update({f'{suffix}/pk': viewset.retrieve_update_delete})


def appeal(uri: str, method: str, data: list):
    if view := paths.get(uri):
        return view()
    else:
        return False


def validate(uri):
    if uri[-1] == '/':
        uri = uri[1:-1].split('/')
    else:
        uri = uri[1:].split('/')
        
    if '' in uri or len(uri) > 2:
        return False

    try:
        int(uri[1])
    except IndexError:
        return uri[0]
    except ValueError:
        return False
    else:
        return f'{uri[0]}/pk'


def direct(uri: str, method: str, data: list):
    if uri == '/':
        return appeal(uri, method, data)
    
    if uri := validate(uri):
        return appeal(uri, method, data)
    else:
        print('404 in distributor.py')
        return False
