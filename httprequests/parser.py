class HTTPParser:
    '''
    Parser for HTTP/1.0 requests.
    '''
    def parse(self, request_data):
        '''
        Parse full request.
        '''
        # create an iterator for request lines
        lines = iter(request_data.split('\r\n'))

        # parse the request line
        method, full_path, version = self._parse_request_line(next(lines))

        # extract path and params if they exist
        path, query_params = self._parse_path(full_path)

        # parse headers
        headers = self._parse_headers(lines)

        # parse body
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
        # will need to check for malformed syntax and version
        return request_data.split()


    def _parse_path(self, full_path):
        '''
        Parse the full path to check for query params.
        '''
        if '?' in full_path:
            # seperate query params from path
            path, query_params = full_path.split('?', 1)
            # seperate key value pairs
            query_params = dict(param.split('=') for param in query_params.split('&'))
        else:
            path = full_path
            query_params = {}
        return path, query_params

    def _parse_headers(self, headers_lines):
        '''
        Parse requests headers
        '''
        # will need to check for malformed syntax
        headers = {}
        for line in headers_lines:
            if line == '':
                break
            # split at the first colon
            k, v = line.split(':', 1)
            headers[k] = v.strip()
        return headers

    def _parse_body(self, body_lines, headers):
        '''
        Parse the request body.
        And check Content-Length
        '''
        # add content length check
        # content_length = int(headers.get('Content-Length'))
        return ''.join(body_lines)
        

    def validate_request(method, path, version, headers, body):
        pass