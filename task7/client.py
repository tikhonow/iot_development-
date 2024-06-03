import socket
import threading
import time

def client_task(host, port, operation, interval):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(operation.encode())
            data = s.recv(1024)
            print(f"Operation: {operation}, Received: {data.decode()}")
        time.sleep(interval)

if __name__ == "__main__":
    host, port = "127.0.0.1", 65432
    threading.Thread(target=client_task, args=(host, port, "add", 1)).start()
    threading.Thread(target=client_task, args=(host, port, "multiply", 10)).start()
