from httprequests.exceptions import *
from utils import MAX_REQUEST_SIZE, VALID_HTTP_1_0_HEADERS


class HTTPParser:
    '''
    Parser for HTTP/1.0 requests.
    '''
    def parse(self, request_data):
        '''
        Parse full request.
        '''
        # Check for empty request.
        if not request_data.strip():
            raise BadRequest(body='Bad Request: Empty Request.')

        # Check if request too long.
        if len(request_data) > MAX_REQUEST_SIZE:
            raise BadRequest(body='Bad Request: Request too long.')

        # Create an iterator for request lines.
        lines = iter(request_data.split('\r\n'))

        # Parse the request line.
        method, full_path, version = self._parse_request_line(next(lines))

        # Extract path and params if they exist.
        path, query_params = self._parse_path(full_path)

        # Parse request headers.
        headers = self._parse_headers(lines)

        # Parse request body.
        body = self._parse_body(lines, headers)

        return {
            'method': method,
            'path': path,
            'query_params': query_params,
            'version': version,
            'headers': headers,
            'body': body
        }

    def _parse_request_line(self, request_data):
        '''
        Parse request line (e.g. GET /doc/test.html HTTP/1.0)
        '''
        try:
            method, full_path, version = request_data.split()
        except ValueError as e:
            raise BadRequest(body='Bad Request: Malformed request line.') from e
        valid_methods = {'GET', 'POST', 'HEAD'}
        if method not in valid_methods:
            raise BadRequest(body=f'Bad Request: Unsupported method {method}.')
        if version != 'HTTP/1.0':
            raise BadRequest(body=f'Bad Request: Unsupported HTTP Version {version}.')
        return method, full_path, version


    def _parse_path(self, full_path):
        '''
        Parse the full path to check for query params.
        '''
        if '?' in full_path:
            # Seperate query params from path.
            path, query_params = full_path.split('?', 1)
            try:
                # Seperate key value pairs.
                query_params = dict(param.split('=') for param in query_params.split('&'))
            except ValueError as e:
                raise BadRequest(body='Bad Request: Malformed query parameters.') from e
        else:
            path = full_path
            query_params = {}
        return path, query_params

    def _parse_headers(self, headers_lines):
        '''
        Parse requests headers
        '''
        headers = {}
        for line in headers_lines:
            if line == '':
                break
            if ':' not in line:
                raise BadRequest(body=f'Bad Request: Malformed header {line}.')
            # Split at the first colon.
            key, value = line.split(':', 1)
            if key not in VALID_HTTP_1_0_HEADERS:
                raise BadRequest(body=f'Bad Request: Invalid header {key}.')
            headers[key] = value.strip()
        return headers

    def _parse_body(self, body_lines, headers):
        '''
        Parse the request body.
        And check Content-Length
        '''
        # Add content length check.
        # content_length = int(headers.get('Content-Length'))
        return ''.join(body_lines)
