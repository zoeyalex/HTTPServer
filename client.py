import socket


def send_request(host, port, path):
    '''
    Sample client code for testing purposes.
    '''
    request = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(request.encode())
    response = s.recv(1024)
    print(response.decode())

if __name__ == '__main__':
    send_request('localhost', 8080, '/')