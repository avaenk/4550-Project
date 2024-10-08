from socket import *
import threading

player_count = 0
player_lock = threading.Lock()  #to cap players

def handle_client(connectionSocket, player_name):
    print(f"{player_name} has joined the game.")
    connectionSocket.send("Welcome to the Trivia Game! Type 'exit' to disconnect.".encode())
    
    global player_count
    while True:
        message = connectionSocket.recv(1024).decode()#message from from player 
        if message.lower() == 'exit':#player leaving game 
            print(f"{player_name} has disconnected.")
            with player_lock:
                player_count -= 1 
                if player_count == 0:
                    print("All players have exited. Game over.")
            break

        #print recieved message to server -- need to add where it displays it to all other clients other than self
        print(f"Received from {player_name}: {message}")
        connectionSocket.send(f"{player_name}, you said: {message}".encode())

    connectionSocket.close()

def run_server():
    global player_count
    serverPort = 13009
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(7)  # Allow up to 5 connections
    
    while True:
        #new connection from player
        connectionSocket, addr = serverSocket.accept()
        
        with player_lock:
            #updating player count when the new connection is added 
            player_count += 1
            player_name = f"Player {player_count}"
        
        #new thread to manage the new connections messages 
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()
