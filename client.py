import socket

HOST = '127.0.0.1'
PORT = 13009

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Get the username message, send back the username, and store it
    username_message = client_socket.recv(1024).decode()
    print(username_message)
    username = input("Enter username: ")
    client_socket.send(username.encode())

    # Main game loop - only prompt when receiving a specific input request
    while True:
        server_message = client_socket.recv(1024).decode()
        print(server_message)  # Display server's message

        # Only ask for input if the server message contains "Your answer:"
        if "Your answer:" in server_message:
            answer = input()
            client_socket.send(answer.encode())

        # Exit condition if the game ends
        if "Game over!" in server_message:
            break

    client_socket.close()

if __name__ == "__main__":
    client()
