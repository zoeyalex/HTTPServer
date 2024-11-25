import socket
import sys
import argparse
from httprequests.parser import HTTPParser
from httprequests.exceptions import *
from httprequests.response_builder import HTTPResponse
from utils import pretty_print_request, MAX_REQUEST_SIZE


class HTTPServer:
    '''
    Simple HTTP 1.0 server.
    available methods GET, POST
    '''
    def __init__(self, host='localhost', port=8080, backlog=1):
        self.host = host
        self.port = port
        # create a listener socket object, sock_stream for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parser = HTTPParser()

    def start(self):
        '''
        Main server loop.
        '''
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
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
        Try to parse the request if available.
        '''
        response = ''
        try:
            request_data = com.recv(MAX_REQUEST_SIZE).decode() # data comes in raw bytes
            ''' 
            check for empty request // MOVED TO PARSER, LEAVE SERVER TO HANDLE 5xx
            if not request_data.strip():
                raise BadRequest(body='Bad Request: Empty Request.')
            '''
            #print pre-parsed data for debugging
            #print(request_data)
            parsed_request = self.parser.parse(request_data)
            print('Parsed request: ')
            pretty_print_request(parsed_request)
            response = HTTPResponse(200, body='OK').build()
        except HTTPException as e:
            response = e.responsify().build()
        except Exception:
            '''
            Unhandled exceptions.
            '''
            response = InternalServerError().responsify().build()

        finally:
            # add newline to avoid terminal problems.
            com.sendall((response+'\n').encode())
            com.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP 1.0 Server")
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind the server to (default: localhost)')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind the server to (default: 8080)')
    parser.add_argument('--backlog', type=int, default=1, help='Socket backlog size (default: 1)')
    args = parser.parse_args()
    server = HTTPServer(args.host, args.port, args.backlog)
    server.start()
