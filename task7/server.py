import socket
import threading

value = 1
lock = threading.Lock()

def handle_client(conn, addr):
    global value
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            operation = data.decode()
            with lock:
                if operation == 'add':
                    value += 1
                elif operation == 'multiply':
                    value *= 2
                print(f"Current value: {value}")
            conn.sendall(str(value).encode())

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started at {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server("127.0.0.1", 65432)
