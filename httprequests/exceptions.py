from httprequests.status_codes import HTTP_STATUS_CODES
from httprequests.response_builder import HTTPResponse


class HTTPException(Exception):
    '''
    Base exception class for HTTP errors.
    '''
    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.message = HTTP_STATUS_CODES.get(status_code, 'Unknown Status')
        self.headers = headers or {}
        self.body = body or f'{status_code} {self.message}'
        super().__init__(f'{status_code} {self.message}')

    def responsify(self):
        '''
        Convert exception into a valid response.
        '''
        return HTTPResponse(
            self.status_code,
            self.headers,
            self.body
        )


class BadRequest(HTTPException):
    '''
    400 Bad Request
    Malformed or invalid request.
    (request line, headers, body not matching Content-Length)
    '''
    def __init__(self, body='Bad Request: Malformed syntax.'):
        super().__init__(400, body=body)


class Unauthorized(HTTPException):
    '''
    401 Unauthorized
    Request requires user authentication.
    If credentials were provided then the 
    401 response indicates that authorization has
    been refused for those credentials.
    ''' 
    def __init__(self, body='Unauthorized: Proper authentication is required for access.'):
        super().__init__(401, body=body)


class Forbidden(HTTPException):
    '''
    403 Forbidden
    Client is not allowed to access resource,
    even with valid authentication.
    '''
    def __init__(self, body='Forbidden.'):
        super().__init__(403, body=body)


class NotFound(HTTPException):
    '''
    404 Not Found
    Requested URI does not exist.
    '''
    def __init__(self, body='Not Found.'):
        super().__init__(404, body=body)


class InternalServerError(HTTPException):
    '''
    500 Internal Server Error
    Unhandled exception.
    '''
    def __init__(self, body='Internal Server Error.'):
        super().__init__(500, body=body)


class NotImplemented(HTTPException):
    '''
    501 Not Implemented
    Server does not support the funcionality
    required to fulfil the request.
    '''
    def __init__(self, body='Not Implemented.'):
        super().__init__(501, body=body)


class BadGateway(HTTPException):
    '''
    502 Bad Gateway
    The server, while acting as a gateway or proxy,
    received an invalid response from the upstream server it accessed
    in attempting to fulfil the request.
    '''
    def __init__(self, body='Bad Gateway.'):
        super().__init__(502, body=body)


class ServiceUnavailable(HTTPException):
    '''
    503 Service Unavailable
    The server is temporarily unable to handle the request.
    Typically due to overload or maintenance.
    '''
    def __init__(self, body='Service Unavailable.'):
        super().__init__(503, body=body)
