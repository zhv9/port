import socket


def get_raw_http_response(host, port, path):
    CRLF = b"\r\n"

    request = [
        b"GET " + path.encode('ascii') + b" HTTP/1.1",
        b"Host: " + host.encode('ascii'),
        b"Connection: Close",
        b"",
        b"",
    ]

    # Connect to the server
    s = socket.socket()
    s.connect((host, port))

    # Send an HTTP request
    s.send(CRLF.join(request))

    # Get the response (in several parts, if necessary)
    response = b''
    buffer = s.recv(4096)
    while buffer:
        response += buffer
        buffer = s.recv(4096)

    return response

# 不加这个Content-Type的话，就无法以json发送数据，服务器就不能用request.get_json()获取json
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json'
           }
