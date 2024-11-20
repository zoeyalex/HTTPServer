class HTTPParser:
    '''
    Parser for HTTP/1.0 requests.
    '''
    def parse(self, request_data):
        '''
        Parse full request.
        '''
        lines = request_data.split('\r\n')
        method, full_path, version = lines[0].split()
        if version != 'HTTP/1.0':
            raise ValueError
        path, query_params = self._parse_path(full_path)
        # add header/body parsing
        return {
            'method': method,
            'path': path,
            'query_params': query_params,
            'version': version,
            'headers': {
                'Host': 'localhost:8080',
                'User-Agent': 'Client/1.0',
                'Content-Type': 'text/plain',
                'Connection': 'Close'
            },
            'body': 'testtest123'
        }

    def _parse_path(self, full_path):
        '''
        Parse the full path to check for query params.
        For internal use only.
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