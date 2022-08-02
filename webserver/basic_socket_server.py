from pathlib import Path
import socket


host = ''
port = 3000
address = (host, port)

parent = Path(__file__).parent

server = socket.socket()
server.bind(address)
with server:
    server.listen()
    print('Server online! Listening for connections.')
    while True:
        client_socket, addr = server.accept()
        with client_socket:
            response = client_socket.recv(1024).decode()
            print(response)
            url_path = response.split(' ')[1]

            file_name = '/index.html'
            file_path = f'{parent}{url_path}{file_name}'

            try:
                with open(file_path) as file:
                    content = file.read()

                response = 'HTTP/1.1 200 OK\n\n' + content
                client_socket.sendall(response.encode())
            except FileNotFoundError:
                response = f'HTTP/1.1 404 NOT FOUND\n\nFile for path **{url_path}** not found'
                client_socket.sendall(response.encode())
