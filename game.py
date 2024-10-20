import threading
from threading import Thread
import time
import random #selecting topic for rounds
from socket import *
from question import question,peopleQuestion, dateQuestion, placeQuestion
from server import clients # imports clients
from server import client_usernames #import client usernames

# TO DO
# Change rounds so they are by topics searched by through our key words
# figure out player class and how can be merged with clients from server
# should i do a check if there is a username associated w socket before appending to players?

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
    return players

def start_game():
    print("Welcome to Breaking News Trivia!")
    global players
    players = create_players()

def run_game():
    start_game()
    for round_num in range(3):
        topic = choose_topic
        print(f"Staring Round {round_num+1}: Topic is {topic}")

        cache = []
        for qnum in range(3):
            print(f"Question {qnum}...")
            question_obj = choose_question(topic, seed)
            ask_question(question_obj)
        print(f"Round {round_num+1} complete")
    print("Game over! Final scores: ")
    display_final_scores()

def choose_topic():
    with open('topic.txt','r') as f:
        topics = f.readlines()
    return random.choice(topics).strip() #chooses random topics, gets rid of newline

def choose_question(topic, seed):
    point_value = 10 #example num points, can change
    return question(topic, point_value, seed)

def ask_question(question_obj):
    #notify players of question
    for player in players:
        player.socket.send(question_obj.getQuestion().encode())
        answers = {}
        all_players_answered = threading.Event()

    def collect_answers():
        for player in players:
            try:
                answer = player.socket.recv(1024).decode() # blocking call
                answers[player.username] = answer # player name corresponds to answer
            except Exception as e:
                print(f"Error receiving answer fro {player.username}: {e}")
                answer[player.username] = "Disconnected" 
        all_players_answered.set() # collected all answers

    # starting answering thread
    answer_thread = Thread(target = collect_answers)
    answer_thread.start()

    # timer starts
    timeout = time.time() + 60
    while time.time() < timeout:
        if all_players_answered.is_set(): 
            break # breaks early if everyone answers bfre timer

    # give each player feedback
    correct_ans = question_obj.getAnswer
    score = question.obj.checkAnswer(answer)
    for player in players: 
        if player.username in answers: #if player answered
            answer = answers[player.username]
            if answer == "Disconnected":
                reponse = f"You have disconnected. The correct answer was: {correct_ans}"
            elif score: # if answer is correct, ie point value>0
                response = f"You correctly answered: {answer}"
                player.update_score(score) # add points
            else:
                response = f"You incorrecly answered: {answer}. The correct answer is: {correct_ans}"
        else: # player didn't answer
            response = f"You timed out. The correct answer is: {correct_ans}"
            
        response += "\nCurrent Score: " + player.score
        player.socket.send(response.encode())
    answer_thread.join() 

def display_final_scores():
    for player in players:
        print(f"{player.username}: {player.score}")



if __name__ == "__main__":
    run_game()

                

