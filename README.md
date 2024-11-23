# HTTP/1.0 Server
## 👷‍♀️ Work in progress 🚧
A simple HTTP/1.0 server written in Python. This project aims to support basic HTTP methods, status codes, and static file serving.
## Features
- Supports the HTTP/1.0 protocol.
- Request parsing.
- Custom exception handling.
- Response builder.
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
python server.py
```
To run the client:
```python
python client.py
```
Or make a request using curl:
```bash
curl --http1.0 -v "http://localhost:8080/query?var1=123&var2=okay" -H "User-Agent: Client/1.0" -H "Accept: application/json"
```