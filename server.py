import socket
import os
import argparse
from determine_mime_type import get_mime_type
from httprequests.parser import HTTPParser
from httprequests.router import Router
from httprequests.exceptions import *
from httprequests.response_builder import HTTPResponse
from utils import pretty_print_request, MAX_REQUEST_SIZE


class HTTPServer:
    '''
    Simple HTTP 1.0 server.
    available methods GET, POST
    '''
    def __init__(self, host='localhost', port=8080, backlog=1, static_dir='static'):
        self.host = host
        self.port = port
        self.backlog = backlog
        # create a listener socket object, sock_stream for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.static_dir = static_dir
        self.parser = HTTPParser()
        self.router = Router()

    def start(self):
        '''
        Main server loop.
        '''
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        print(f'Server running on {self.host}:{self.port}')
        try:
            while True:
                # communication socket and address
                com, addr = self.sock.accept() 
                print(f'Connected by {addr[0]}:{addr[1]}' )
                self.handle_connection(com)
        except KeyboardInterrupt:
            print('\nShutting down server.')

    def handle_connection(self, com):
        '''
        Handle the connection with client.
        Try to parse and process the request if possible.
        '''
        response = ''
        try:
            request_data = com.recv(MAX_REQUEST_SIZE).decode() # data comes in raw bytes
            parsed_request = self.parser.parse(request_data)

            print('Parsed request: ')
            pretty_print_request(parsed_request)
            print('\n')

            response = self.process_request(parsed_request)
        except HTTPException as e:
            response = e.responsify().build()
        except Exception:
            '''
            Unhandled exceptions.
            '''
            response = InternalServerError().responsify().build()
        finally:
            com.sendall((response))
            com.close()

    def process_request(self, parsed_request):
        '''
        Process static files and resolve route.
        '''
        method = parsed_request['method']
        path = parsed_request['path']

        # Attempt to resolve dynamic route
        if self.router.has_route(path):
            route = self.router.resolve(path)
            allowed_methods = route['allowed_methods']
            if method not in allowed_methods:
                raise NotImplemented(body=f'Method {method} Not Allowed for {path}.')
            handler = route['handler']
            return handler(parsed_request)
        # Serve static file
        file_path =  self.resolve_static_path(path)
        return self.serve_file(file_path)

    def resolve_static_path(self, path):
        '''
        Map the requested path to a file path in the static directory.
        '''
        temp = path
        if path.startswith(f'/{self.static_dir}/'):
            return os.path.abspath(os.path.normpath(path.lstrip('/')))
        raise NotFound(body='File Not Found.')

    def serve_file(self, file_path):
        '''
        Serve a static file.
        '''
        try:
            if not os.path.isfile(file_path):
                raise NotFound(body='File Not Found.')

            with open(file_path, 'rb') as f:
                content = f.read()
                mime_type = get_mime_type(file_path, content)

            headers = {'Content-Type': mime_type}
            return HTTPResponse(200, headers=headers, body=content).build()
        except NotFound as e:
            raise e
        except Exception as e:
            print(f"Unexpected error while serving file {file_path}: {e}")
            raise InternalServerError(body='Internal Server Error while serving file.') from e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP 1.0 Server')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind the server to (default: localhost)')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind the server to (default: 8080)')
    parser.add_argument('--backlog', type=int, default=1, help='Socket backlog size (default: 1)')
    args = parser.parse_args()

    server = HTTPServer(args.host, args.port, args.backlog)

    # add dynamic user-defined routes
    def handle_submit(request):
        '''
        Handle form submission via POST.
        '''
        body = request['body']
        return HTTPResponse(200, body=f'Form data received: {body}').build()

    def handle_api(request):
        '''
        Handle API resource via GET.
        '''
        query_params = request.get('query_params', {})
        print(query_params)
        return HTTPResponse(200, body=f'API response with params: {query_params}').build()

    server.router.add_route('/submit', handle_submit, allowed_methods=['POST'])
    server.router.add_route('/api/resource', handle_api, allowed_methods=['GET'])

    server.start()
