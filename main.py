import threading 
from server import run_server, get_player_count
from game import run_game
import time

def main():
    #this will create a new thread to run the start server function froms server.py 
    #server can then run
    server_thread = threading.Thread(target=run_server)
    #starting the server thread so it can invoke the function in a diff thread
    server_thread.start()
    print("Game has started. Waiting for players to join")
    
    required_players = 2
    prev_curr_players = 0

    while get_player_count() <= required_players:
        if prev_curr_players < get_player_count(): #only print statement once there is a change in # players
            prev_curr_players = get_player_count() 
            print(f"Current number of players {get_player_count()}")
            print(f"You need {required_players-get_player_count()} more player(s)")
        time.sleep(5)
        if (get_player_count() == required_players): # if you have the amount you need break and run game
            break
    
    run_game()    

main()