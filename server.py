from socket import *
import threading

player_count = 0
player_lock = threading.Lock()
broadcast_lock = threading.Lock() 
clients = []
client_usernames = {}
all_answers = {}
all_answers_event = threading.Event()

# Broadcast all answers once all players have submitted
def broadcast_round_results():
    with broadcast_lock:  
        round_message = "Player answers for this round are:\n"
        for player, answer in all_answers.items():
            round_message += f"{player}: {answer}\n" 

        # Send the combined message to all clients
        for client in clients:
            client.send(round_message.encode())

# Handle communication with each specific client
def handle_client(connection_socket, player_name):
    global player_count
    print(f"{player_name} has joined the game.")
    connection_socket.send("Welcome to the Trivia Game! Type 'exit' to disconnect.".encode())

    while True:
        try:
            message = connection_socket.recv(1024).decode()
            if not message:
                break
            if message.lower() == 'exit':
                disconnect_player(connection_socket, player_name)
                break

            # Store answer
            all_answers[player_name] = message
            print(f"Received answer from {player_name}: {message}")

            # Check if all players have answered
            with player_lock:
                if len(all_answers) == player_count:
                    broadcast_round_results()  # Broadcast once all answers are collected
                    all_answers.clear()  # Clear answers for next round

        except:
            break

    connection_socket.close()

def disconnect_player(connection_socket, player_name):
    print(f"{player_name} has disconnected.")
    with player_lock:
        global player_count
        player_count -= 1
        clients.remove(connection_socket)
    connection_socket.close()

def run_server():
    global player_count
    server_port = 13009
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(7)

    while True:
        connection_socket, addr = server_socket.accept()
        with player_lock:
            connection_socket.send("Enter desired username or enter * to have one chosen for you: ".encode())
            user_message = connection_socket.recv(1024).decode()
            player_name = f"Player {player_count + 1}" if user_message == '*' else user_message
            player_count += 1

            clients.append(connection_socket)
            client_usernames[connection_socket] = player_name

        client_thread = threading.Thread(target=handle_client, args=(connection_socket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()
