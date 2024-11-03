import socket

HOST = '127.0.0.1'
PORT = 13009

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Get the username message, send back the username, and store it
    username_message = client_socket.recv(1024).decode()
    print(username_message)
    username = input()
    client_socket.send(username.encode())

    start_message = client_socket.recv(1024).decode()
    print(start_message)

    # Use the provided username for prompts
    while True:
        message = input(f"{username}: ")
        client_socket.send(message.encode())

        if message.lower() == 'exit':
            break

        # Wait to receive the synchronized response with newlines
        response = client_socket.recv(1024).decode()
        print(response)

    client_socket.close()

if __name__ == "__main__":
    client()
