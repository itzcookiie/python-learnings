import socket

host = ''
port = 3000
address = (host, port)

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

            if url_path == '/' or url_path == '/favicon.ico':
                file_path = 'index.html'
            else:
                file_path = f'{url_path[1:]}.html'

            try:
                with open(file_path) as file:
                    content = file.read()

                response = 'HTTP/1.1 200 OK\n\n' + content
                client_socket.sendall(response.encode())
            except FileNotFoundError:
                response = f'HTTP/1.1 404 NOT FOUND\n\nFile for path **{url_path}** not found'
                client_socket.sendall(response.encode())
