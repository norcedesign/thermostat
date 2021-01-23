import socket


def connect(host: str = 'localhost', port: int = 1234) -> socket:
    screen: socket

    screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen.connect((host, port))

    return screen
