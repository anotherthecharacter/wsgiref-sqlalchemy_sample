class RoutingError(Exception):

    def __str__(self) -> str:
        return 'An error occurred while routing the URLs. Perhaps you have inserted a slashes "/" into suffixes?'


class HTTP404(Exception):
    pass


def get_object_or_404(model, pk, session):
    try:
        session.query(model).filter(model.id==pk)[0]
    except IndexError:
        raise HTTP404
    else:
        return session.query(model).filter(model.id==pk)
