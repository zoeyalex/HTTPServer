import socket


class Server:
    '''
    Simple HTTP 1.0 server.
    available methods GET, POST
    '''
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        # create a listener socket object, sock_stream for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        request_data = com.recv(1024).decode() # data comes in raw bytes
        if not request_data:
            return
        print(request_data)

        response = (
                    'HTTP/1.0 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    'Content-Length: 13\r\n'
                    '\r\n'
                    'Hello, World!'
                )
        com.sendall(response.encode())
        com.close()

    def parse_request(self, request_data):
        pass

if __name__ == '__main__':
    server = Server()
    server.start()