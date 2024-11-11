from socket import *
import threading

clients = []
client_usernames = {}

player_lock = threading.Lock()
player_count = 0

# Handle client connection setup only
def handle_client_setup(connection_socket):
    global player_count
    connection_socket.send("Enter desired username or enter * to have one chosen for you: ".encode())
    user_message = connection_socket.recv(1024).decode().strip()
    
    with player_lock:
        player_name = f"Player {player_count + 1}" if user_message == '*' else user_message
        client_usernames[connection_socket] = player_name
        player_count += 1

    # Send a welcome message to acknowledge the setup; no prompt for input yet
    connection_socket.send(f"Welcome to the Trivia Game, {player_name}! Please wait for the game to begin.\n".encode())
    clients.append(connection_socket)

def run_server():
    global player_count
    server_port = 13009
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(7)

    print("Server started and awaiting player connections...")

    while True:
        connection_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_setup, args=(connection_socket,))
        client_thread.start()

# To get player count for game start check
def get_player_count():
    global player_count
    return player_count

if __name__ == "__main__":
    run_server()