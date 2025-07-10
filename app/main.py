import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True) # wait for client
    client_socket,_=server_socket.accept()

    while True:
        request: bytes = client_socket.recv(1024)
        data: bytes = request.decode()

        if "ping" in data.lower():
            client_socket.send("+PONG\r\n".encode())
    

if __name__ == "__main__":
    main()
