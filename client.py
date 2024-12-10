import socket
import argparse
from PIL import Image


def send_request(host, port, method, path, headers=None, body=None):
    '''
    Sample client code for testing purposes.
    '''
    headers = headers or {}
    headers['Host'] = host
    headers['User-Agent'] = 'PythonClient/1.0'

    request = f'{method.upper()} {path} HTTP/1.0\r\n'

    for key, value in headers.items():
        request += f'{key}: {value}\r\n'
    
    if body:
        headers['Content-Length'] = str(len(body))
        request += f'\r\n{body}'
    else:
        request += '\r\n'

    print(f'Request sent:\n{request}\n')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(request.encode())
    response = b''
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        response += chunk
    s.close()

    headers, _, body = response.partition(b'\r\n\r\n')
    body = body or b''  # Ensure body is a byte string

    print("Response Headers:\n")
    print(headers.decode(errors='replace'))

    if b'Content-Type: ' in headers and b'text/' in headers:
            try:
                print("\nResponse Body:\n")
                print(body.decode(errors='replace'))
            except UnicodeDecodeError as e:
                print(f"Error decoding body: {e}")
    else:
        print("\nResponse Body (binary data detected):\n")
        print(f"{len(body)} bytes received (not displayed).")
        with open('temp.jpg', 'wb') as f:
            f.write(body)
        try:
            image = Image.open('temp.jpg')
            image.show()
        except Exception as e:
            print(f'Error displaying image: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP 1.0 Client")
    parser.add_argument('method', type=str, help='HTTP method')
    parser.add_argument('path', type=str, help='Resource path')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind the server to (default: localhost)')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--headers', type=str, nargs='*', help='Request headers')
    parser.add_argument('--body', type=str, help='Request body')
    args = parser.parse_args()
    headers = {}
    if args.headers:
        for header in args.headers:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
            else:
                print(f"Invalid header format: {header}. Headers should be in key:value format.")
                raise Exception
    send_request(args.host, args.port, args.method, args.path, headers, args.body)