from socket import *

def client():
    serverName = '127.0.0.1'
    serverPort = 13009

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    username_message = clientSocket.recv(1024).decode()
    print(username_message)

    username = input() 
    clientSocket.send(username.encode()) 

    start_message = clientSocket.recv(1024).decode()
    print(start_message)

    while True:
        message = input("You: ")  
        clientSocket.send(message.encode())  
        
        if message.lower() == 'exit':
            break

        response = clientSocket.recv(1024).decode()
        print(response)

    clientSocket.close()

if __name__ == "__main__":
    client()
