from socket import *
import threading

player_count = 0
player_lock = threading.Lock()  # to cap players

def handle_client(connectionSocket, player_name):
    print("{} has joined the game.".format(player_name))
    connectionSocket.send("Welcome to the Trivia Game! Type 'exit' to disconnect.".encode())
    
    global player_count
    while True:
        message = connectionSocket.recv(1024).decode()  # message from player 
        if message.lower() == 'exit':  # player leaving game 
            print("{} has disconnected.".format(player_name))
            with player_lock:
                player_count -= 1 
                if player_count == 0:
                    print("All players have exited. Game over.")
            break

        # print received message to server -- need to add where it displays it to all other clients other than self
        print("Received from {}: {}".format(player_name, message))
        connectionSocket.send("{} you said: {}".format(player_name, message).encode())

    connectionSocket.close()

def run_server():
    global player_count
    serverPort = 13009
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(7)  # allow up to 5 connections
    
    while True:
        # new connection from player
        connectionSocket, addr = serverSocket.accept()
        
        with player_lock:  # updating player count when the new connection is added 
            player_count += 1
            player_name = "Player {}".format(player_count)
        
        # new thread to manage the new connections messages 
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()  # starting the server
