import socket  # noqa: F401
import threading  # noqa: F401

BUF_SIZE = 4096  # Buffer size for receiving data
def handle_command(
    args: list, database: DatabaseHandler, expirations_manager: ExpirationManager
) -> str:
    if len(args) != 1 or len(args[0]) == 0:  # Error if no argument is provided
        return "-ERR wrong number of arguments for command\r\n"
    return f"${len(args[0])}\r\n{args[0]}\r\n"

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
