from status_codes import HTTP_STATUS_CODES
class HTTPException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code
        self.message = HTTP_STATUS_CODES.get(status_code, 'Unknown Status')
        super().__init__(f'{status_code} {self.message}')


class BadRequest(HTTPException):
    '''
    400 Bad Request
    Malformed or invalid request.
    (request line, headers, body not matching Content-Length)
    '''
    def __init__(self):
        super().__init__(400)


class Unauthorized(HTTPException):
    '''
    401 Unauthorized
    Request requires user authentication.
    If credentials were provided then the 
    401 response indicates that authorization has
    been refused for those credentials.
    ''' 
    def __init__(self):
        super().__init__(401)


class Forbidden(HTTPException):
    '''
    403 Forbidden
    Client is not allowed to access resource,
    even with valid authentication.
    '''
    def __init__(self):
        super().__init__(403)


class NotFound(HTTPException):
    '''
    404 Not Found
    Requested URI does not exist.
    '''
    def __init__(self):
        super().__init__(404)


class InternalServerError(HTTPException):
    '''
    500 Internal Server Error
    Unhandled exception.
    '''
    def __init__(self):
        super().__init__(500)


class NotImplemented(HTTPException):
    '''
    501 Not Implemented
    Server does not support the funcionality
    required to fulfil the request.
    '''
    def __init__(self):
        super().__init__(501)


class BadGateway(HTTPException):
    '''
    502 Bad Gateway
    The server, while acting as a gateway or proxy,
    received an invalid response from the upstream server it accessed
    in attempting to fulfil the request.
    '''
    def __init__(self):
        super().__init__(502)


class ServiceUnavailable(HTTPException):
    '''
    503 Service Unavailable
    The server is temporarily unable to handle the request.
    Typically due to overload or maintenance.
    '''
    def __init__(self):
        super().__init__(503)