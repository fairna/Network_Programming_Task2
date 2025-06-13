import socket

def start_client():
    server_ip = 'localhost'
    server_port = 45000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

        while True:
            command = input("\n\rCommand (TIME / QUIT): ").strip()
            full_command = f"{command}\r\n"
            client_socket.sendall(full_command.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8').strip()
            print(f"{response}")

            if command == "QUIT":
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
