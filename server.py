from socket import *
import threading

player_count = 0
player_lock = threading.Lock() 
clients = [] 


#handle_client: this will be for the communication for the server one the specfic client
#does so by running a diff thread for each client and this lets our server handle multiple clients at one.
def handle_client(connection_socket, player_name):
    print("{} has joined the game.".format(player_name))
    connection_socket.send("Welcome to the Trivia Game! Type 'exit' to disconnect.".encode())

    global player_count
    while True:
        try:
            message = connection_socket.recv(1024).decode()  
            if not message:  
                break

            if message.lower() == 'exit':  #for players exiting game
                print("{} has disconnected.".format(player_name))
                with player_lock:
                    player_count -= 1
                    clients.remove(connection_socket)  
                    connection_socket.close()  #lose the connection
                break  

            
            print("{}: {}".format(player_name, message))#when the client sends message, this is when they can see the other clients message
            #if they have no sent a message yet they cannot see all the other clients messages
            for client in clients:
                if client != connection_socket:  
                    client.send("{}: {}".format(player_name, message).encode())

        except:
            break  
    connection_socket.close()


#run_server: run_server will set up our server and accept the new client connections -- while keeping the max of 7 players
#this is where the indiivdual threads to be used for handle_clienty will be created
#basicially here we are initialzing the server and waiting/listening for connections from clients. 
def run_server():
    global player_count
    server_port = 13009
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    
    server_socket.listen(7)  #max players 7
    
    while True:
         # new connection from player
        connection_socket = server_socket.accept()

        with player_lock: #they can now pick their username or have a generic Player1..Player2..PlayerN
            connection_socket.send("Enter desired username or enter * to have one chosen for you: ".encode())
            user_message = connection_socket.recv(1024).decode()  
            player_count += 1 # updating player count when the new connection is added 
            if user_message == '*':  
                player_name = "Player {}".format(player_count)
            else:
                player_name = user_message  
            
            clients.append(connection_socket)  

         # new thread to manage the new connections messages 
        client_thread = threading.Thread(target=handle_client, args=(connection_socket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()  
