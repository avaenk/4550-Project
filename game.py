import threading
import time
import random # selecting topic for rounds
from socket import *
from question import question
from server import clients, client_usernames # imports clients and usernames

# To do
# Display a countdown to let players know how much time left when gets to 3 seconds
# add analytics to player class: track best round, average response time, accuracy percentage
# tiebreaker question
# every round feedback: current score, points gained in round, questions correct

# Extra
# implement ability for players to choose number of rounds
# choose difficulty level?

# Issues
# Needs to type something in chat in order to see the questions

questions = [
    "What is a childhood snack that is now part of a chamoy pickle kit?",
    "What is a group of crows called?",
    "Which search algorithm is Goldwassers favorite child? DFS or BFS?"
]
answers = [
    "gushers",
    "murder",
    "DFS"
]


round_number = 0

# Player class to track socket, username, and score
class Player:
    def __init__(self, socket, username):
        self.socket = socket
        self.username = username
        self.score = 0  # Initialize the score

    def __repr__(self): # if object printed (string representation)
        return f"Player(username = {self.username}, score = {self.score})"

    def update_score(self,points):
        self.score += points

def create_players():
    players = []
    for client_socket in clients:
        username = client_usernames.get(client_socket) 
        player = Player(client_socket, username)
        players.append(player)
        print(player) # debug
    return players

def start_game():
    print("Welcome to Breaking News Trivia!")
    global players
    players = create_players()

def run_game():
    print("You are in the game file") # DEBUG ------------------------------------------------------------------------------------------------------------------
    start_game()
    for round_num in range(3):
        topic = choose_topic()
        print(f"Starting Round {round_num+1}: Topic is {topic}")

        cache = []
        for qnum in range(3):
            print(f"Question {qnum+1}...")
            # question_obj = choose_question(topic) DEBUG REAL CODE ---------------------------------------------------------------------------------------
            # ask_question(question_obj) DEBUG REAL CODE --------------------------------------------------------------------------------------------------
            ask_question(questions[qnum]) #TEST CODE ____________________________________________________________________________________________________
        print(f"Round {round_num+1} complete")
    print("Game over! Final scores: ")
    display_final_scores()

def choose_topic():
    with open('topic.txt','r') as f:
        topics = f.readlines()
    return random.choice(topics).strip() #chooses random topics, gets rid of newline

def choose_question(topic):
    point_value = 10 #example num points, can change
    return question(topic, point_value)

def ask_question(question_obj):
    #notify players of question
    for player in players:
        print("in ask_question function") # DEBUG _______________________________________________________________________________________________________
        # player.socket.send(question_obj.getQuestion().encode()) # REAL CODE ---------------------------------------------------------------------------
        player.socket.send(question_obj.encode()) # TEST CODE ____________________________________________________________________________________________
        answers = {}
        all_players_answered = threading.Event()

    def collect_answers():
        for player in players:
            try:
                print("In collect_answers") # DEBUG
                answer = player.socket.recv(1024).decode() # blocking call
                answers[player.username] = answer # player name corresponds to answer
            except Exception as e:
                print(f"Error receiving answer from {player.username}: {e}")
                answer[player.username] = "Disconnected" 
        all_players_answered.set() # collected all answers

    # starting answering thread
    print("About to run collect_answers") # DEBUG
    answer_thread = threading.Thread(target = collect_answers)
    answer_thread.start()

    # timer starts
    timeout = time.time() + 60
    while time.time() < timeout:
        if all_players_answered.is_set(): 
            print("Everyone has answered before the timer") # DEBUG
            break # breaks early if everyone answers bfre timer
    print("about to give feedback") # DEBUG
    # give each player feedback
    # correct_ans = question_obj.getAnswer() # DEBUG REAL CODE ---------------------------------------------------------------------------------------------------------
    # score = question.obj.checkAnswer(answer) # DEBUG REAL CODE -------------------------------------------------------------------------------------------------------
    correct_ans = answers[round_number] # TEST CODE _________________________________________________________________________________________________________________
    score = (correct_ans == answer) # Test Code ______________________________________________________________________________________________________________________
    print(f"this is checking if score works correctly, should be boolean scored or didn't score: {score}") # TEST CODE ________________________________________________________________________________________
    
    for player in players: 
        if player.username in answers: #if player answered
            answer = answers[player.username]
            if answer == "Disconnected":
                reponse = f"You have disconnected. The correct answer was: {correct_ans}"
            elif score: # if answer is correct, ie point value>0
                response = f"You correctly answered: {answer}"
                # player.update_score(score) # add points # DEBUG REAL CODE --------------------------------------------------------------------------------------------
                player.update_score(10) # TEST CODE _____________________________________________________________________________________________________________________________
            else:
                response = f"You incorrectly answered: {answer}. The correct answer is: {correct_ans}"
        else: # player didn't answer
            response = f"You timed out. The correct answer is: {correct_ans}"
            
        response += "\nCurrent Score: " + player.score
        player.socket.send(response.encode())
    answer_thread.join() 

def display_final_scores():
    for player in players:
        player.socket.send(f"{player.username: {player.score}}".encode())  # displays to each client
        print(f"{player.username}: {player.score}") # displays to server



if __name__ == "__main__":
    run_game()

                

