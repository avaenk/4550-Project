from socket import *

def client():
    serverName = '127.0.0.1'
    serverPort = 13011

    #socket for the client & connect to server using IP and port number
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #start message from server to be displayed to each new player(client)
    start_message = clientSocket.recv(1024).decode()
    print(start_message)

    while True:
        message = input("You: ") # change this to playername i.e. player  1 -- agian needs to not send to self, it currently does. 
        clientSocket.send(message.encode())#send player message to server -- it also needs to be sent to other clients ADD 
        
        if message.lower() == 'exit':
            break

        #servers response to previous message 
        response = clientSocket.recv(1024).decode()
        print(response)

    clientSocket.close()

if __name__ == "__main__":
    client()
