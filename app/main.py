import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    import threading

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    def parse_redis_command(data):
        # Minimal RESP parser for arrays of bulk strings
        if not data or not data.startswith(b"*"):
            return None
        try:
            lines = data.split(b"\r\n")
            argc = int(lines[0][1:])
            argv = []
            i = 1
            while i < len(lines) and len(argv) < argc:
                if lines[i].startswith(b"$"):
                    length = int(lines[i][1:])
                    arg = lines[i + 1]
                    argv.append(arg.decode("utf-8"))
                    i += 2
                else:
                    i += 1
            return argv
        except Exception:
            return None

    def handle_client(connection):
        buffer = b""
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                buffer += data
                # Try to parse a command from the buffer
                cmd = parse_redis_command(buffer)
                if cmd:
                    if len(cmd) > 0 and cmd[0].lower() == "ping":
                        connection.sendall(b"+PONG\r\n")
                    elif len(cmd) > 1 and cmd[0].lower() == "echo":
                        # RESP bulk string reply: $<len>\r\n<str>\r\n
                        arg = cmd[1]
                        resp = f"${len(arg)}\r\n{arg}\r\n".encode("utf-8")
                        connection.sendall(resp)
                    buffer = b""  # Clear buffer after handling one command
            except Exception:
                break
        connection.close()

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(connection,), daemon=True)
        thread.start()


if __name__ == "__main__":
    main()