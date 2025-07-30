import socket  # noqa: F401
import threading
import time
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    

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
    store={}
    expiry={}
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
                    command= cmd[0].lower()
                    if command== "ping":
                        connection.sendall(b"+PONG\r\n")
                    elif command == "echo":
                        # RESP bulk string reply: $<len>\r\n<str>\r\n
                        arg = cmd[1]
                        resp = f"${len(arg)}\r\n{arg}\r\n".encode("utf-8")
                        connection.sendall(resp)
                    elif command == "set" and len(cmd) > 2:
                        key, value = cmd[1], cmd[2]
                        px = None
                        i=3
                        while i+1<len(cmd):
                            if cmd[i].lower()=="px":
                                try:
                                    px = int(cmd[i+1])
                                except Exception:
                                    pass
                                break
                            i += 2
                        store[key] = value
                        if px is not None:
                            expiry[key] = time.time() + px / 1000.0
                        elif key in expiry:
                            del expiry[key]
                        connection.sendall(b"+OK\r\n")
                    elif command == "get" and len(cmd) > 1:
                        key = cmd[1]
                        now = time.time()
                        if key in expiry and now>=expiry[key]:
                            if key in store:
                                del store[key]
                            del expiry[key]
                        if key in store:
                            value = store[key]
                            resp = f"${len(value)}\r\n{value}\r\n".encode("utf-8")
                            connection.sendall(resp)
                        else:
                            connection.sendall(b"$-1\r\n")
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