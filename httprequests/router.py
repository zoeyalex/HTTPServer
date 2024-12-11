from httprequests.exceptions import NotFound


class Router:
    '''
    Router for managing and resolving HTTP routes.
    '''
    def __init__(self):
        self.routes = {} # path: (handler, allowed_methods)

    def add_route(self, path, handler, allowed_methods=None):
        '''
        Add a new route
        '''
        self.routes[path] = {
            'handler': handler,
            'allowed_methods': allowed_methods or ['GET']
        }

    def resolve(self, path):
        '''
        Resolve path to handler.
        '''
        if path in self.routes:
            return self.routes[path]
        raise NotFound(body=f'Not Found: {path}.')

    def has_route(self, path):
        '''
        Returns whether path is mapped to a route.
        '''
        return path in self.routes
