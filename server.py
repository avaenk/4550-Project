from socket import *
import threading

#changes that need to be made to this file
#1. currently the client messages are only going to the server, not to the other clients make changes i think? 
# or do we only want it going to the server i am not sure? 
#2. its probably best when a player joins the game they can decidie between the general 
# player1 or they can enter a username we can easily add this. Right now we just have the player count variable,
# we can add an array ?? idk if you do arrays in python, maybe a dictioanry with the client thread and then the name they decide on.  

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
        print("{}: {}".format(player_name, message))
        connectionSocket.send("{}: {}".format(player_name, message).encode())

    connectionSocket.close()

def run_server():
    global player_count
    serverPort = 13011
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(7)  # allow up to 5 connections
    
    while True:
        # new connection from player
        connectionSocket, addr = serverSocket.accept()


        #this is where we can implement changes for the player name choice or the player count
        with player_lock:  # updating player count when the new connection is added 
            player_count += 1
            player_name = "Player {}".format(player_count)
        
        # new thread to manage the new connections messages 
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()  # starting the server
