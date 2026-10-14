
import socket
from datetime import datetime
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8000

folder = Path("request")
folder.mkdir(exist_ok=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Socket server listening on port {PORT}")

    while True:
        connection, address = server.accept()

        with connection:
            connection.settimeout(5)
            chunks = []

            try:
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break

                    chunks.append(data)

                    if b"\r\n\r\n" in b"".join(chunks):
                        break

            except socket.timeout:
                pass

            request_data = b"".join(chunks)

            if request_data:
                filename = folder / (
                    datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
                    + ".bin"
                )

                filename.write_bytes(request_data)

                print(f"Request saved: {filename}")

            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 2\r\n"
                b"Connection: close\r\n"
                b"\r\n"
                b"OK"
            )

            connection.sendall(response)
