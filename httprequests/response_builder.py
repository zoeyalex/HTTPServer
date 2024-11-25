from datetime import datetime
import platform
from httprequests.status_codes import HTTP_STATUS_CODES


class HTTPResponse:
    '''
    Response builder for HTTP/1.0 requests
    '''
    def __init__(self, status_code, headers=None, body=''):
        self.status_code = status_code
        self.reason = HTTP_STATUS_CODES.get(status_code, "Unknown Status")
        self.headers = headers or {}
        self.body = body or ''

    def build(self):
        '''
        Build a HTTP response.
        '''
        # Add Server headers.
        self.headers["Server"] = _generate_server_header()
        self.headers["Date"] = _generate_date_header()

        # Add Content-Length header
        self.headers["Content-Length"] = str(len(self.body))
        self.headers["Content-Type"] = self.headers.get("Content-Type", "text/plain")

        # Build headers string
        headers_str = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())

        # Return full response
        return f"HTTP/1.0 {self.status_code} {self.reason}\r\n{headers_str}\r\n\r\n{self.body}"


def _generate_server_header():
    '''
    Generate the 'server' header.
    '''
    server_name = 'HTTPServer1.0'
    os_info = platform.system()
    python_version = platform.python_version()
    return f'{server_name} ({os_info}/Python{python_version})'

def _generate_date_header():
    '''
    Generate the 'date' header in HTTP-date format.
    '''
    return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
