# HTTP/1.0 Server
## 👷‍♀️ Work in progress 🚧
A simple HTTP/1.0 server written in Python.
## Features
- Request parsing.
- Custom exception handling.
- Custom response builder.
- Static file serving.
## HTTP Methods Supported
`GET`,`POST`,`HEAD`    
## HTTP Status Codes
| 2xx|3xx|4xx|5xx|
|----------------|--------|----|------|
|`200 OK`|`301 Moved Permanently`|`400 Bad Request`|`500 Internal Server Error`|
|`201 Created`|`302 Moved Temporarily`|`401 Unauthorized`|`501 Not Implemented`|
|`202 Accepted`|`304 Not Modified`|`403 Forbidden`|`503 Bad Gateway`|
|`204 No Content`||`404 Not Found`|`503 Service Unavailable`|
## Usage
To run the server:
```bash
usage: server.py [-h] [--host HOST] [--port PORT] [--backlog BACKLOG]

HTTP 1.0 Server

options:
  -h, --help         show this help message and exit
  --host HOST        Host to bind the server to (default: localhost)
  --port PORT        Port to bind the server to (default: 8080)
  --backlog BACKLOG  Socket backlog size (default: 1)
```
To run the client:
```python
python client.py
```
Or make a request using curl:
```bash
curl --http1.0 -v "http://localhost:8080/resource?param1=value1&param2=value2" -H "User-Agent: MyClient/1.0" -H "Accept: application/xml"
```