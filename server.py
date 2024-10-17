from socket import *
import threading

player_count = 0
player_lock = threading.Lock() 
clients = [] 

def handle_client(connectionSocket, player_name):
    print("{} has joined the game.".format(player_name))
    connectionSocket.send("Welcome to the Trivia Game! Type 'exit' to disconnect.".encode())

    global player_count
    while True:
        try:
            message = connectionSocket.recv(1024).decode()  
            if not message:  
                break

            if message.lower() == 'exit':  
                print("{} has disconnected.".format(player_name))
                with player_lock:
                    player_count -= 1
                    clients.remove(connectionSocket)  
                    connectionSocket.close()  
                break  

            
            print("{}: {}".format(player_name, message))
            for client in clients:
                if client != connectionSocket:  
                    client.send("{}: {}".format(player_name, message).encode())

        except:
            break  
    connectionSocket.close()

def run_server():
    global player_count
    serverPort = 13009
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    
    serverSocket.listen(7)  
    
    while True:
        connectionSocket, addr = serverSocket.accept()

        with player_lock:  
            connectionSocket.send("Enter desired username or enter * to have one chosen for you: ".encode())
            user_message = connectionSocket.recv(1024).decode()  
            player_count += 1
            if user_message == '*':  
                player_name = "Player {}".format(player_count)
            else:
                player_name = user_message  
            
            clients.append(connectionSocket)  

        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, player_name))
        client_thread.start()

if __name__ == "__main__":
    run_server()  
