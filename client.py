from socket import *


#client: starts the connection with the server --> from the client side 
# also intercats with the server, here is where we get the username, although we are saving it in the server 
#we are handling the clients user input here 
def client():
    server_name = '127.0.0.1'
    server_port = 13009

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    username_message = client_socket.recv(1024).decode()
    print(username_message) 
    #where the client is prompted to choose username or have generic one

    username = input() 
    client_socket.send(username.encode()) 

    start_message = client_socket.recv(1024).decode()
    print(start_message)

    while True:#send the player message when we implement more this will be where they are putting their answer. 
        message = input("You: ")  
        client_socket.send(message.encode())  
        
        if message.lower() == 'exit':
            break

        #servers reponse to message -- here is where we would have the response of correct/incorrect etc. 
        response = client_socket.recv(1024).decode()
        print(response)

    client_socket.close()

if __name__ == "__main__":
    client()
