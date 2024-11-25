import socket


def send_request(host, port, path):
    '''
    Sample client code for testing purposes.
    '''
    ua='CustomClient/1.0'
    body='name=John&age=30&city=London'
    #request = f'GET {path} HTTP/1.0\r\nHost: {host}\r\nUserAgent: {UA}\r\n\r\n'
    #request = f'POST {path} HTTP/1.0\r\nHost: {host}\r\nUserAgent: {ua}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nname=John&age=30&city=London'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(request.encode())
    response = s.recv(1024)
    print(response.decode())

if __name__ == '__main__':
    send_request('localhost', 8080, '/submit?user=John&id=123')