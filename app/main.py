import socket  # noqa: F401
import threading  # noqa: F401

BUF_SIZE = 4096  # Buffer size for receiving data
def handle_command(client: socket.socket):
    while chunk:=client.recv(BUF_SIZE):
        if chunk==b"":
            break
        client.sendall(b"+PONG\r\n")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True) # wait for client
    # client_socket,_=server_socket.accept()

    while True:
        client_socket,client_arr= server_socket.accept()
        threading.Thread(target=handle_command, args=(client_socket,)).start()
    

if __name__ == "__main__":
    main()
