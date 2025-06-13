from socket import *
import socket
import threading
import logging
import datetime

logging.basicConfig(level=logging.WARNING)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                data = self.connection.recv(1024)
                if data:
                    decoded = data.decode('utf-8').strip()
                    logging.warning(f"Received from {self.address}: {decoded}")

                    if decoded == "QUIT":
                        logging.warning(f"\r\n")
                        break

                    if decoded.startswith("TIME"):
                        now = datetime.datetime.now()
                        time_str = now.strftime("%H:%M:%S")
                        response = f"JAM {time_str}\r\n"
                        self.connection.sendall(response.encode('utf-8'))
                    else:
                        error_msg = "ERROR Unknown command\r\n"
                        self.connection.sendall(error_msg.encode('utf-8'))
                else:
                    break
            except Exception as e:
                logging.warning(f"Error with client {self.address}: {e}")
                break

        self.connection.close()
        logging.warning(f"Connection closed for {self.address}")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        logging.warning("Server is running on port 45000")
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"\n\nConnection from {self.client_address}")
            
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
