import threading 
from server import run_server

def main():
    #this will create a new thread to run the start server function froms server.py 
    #server can then run
    server_thread = threading.Thread(target=run_server)
    #starting the server thread so it can invoke the function in a diff thread
    server_thread.start()
    print("Game has started. Waiting for players to join")

main()