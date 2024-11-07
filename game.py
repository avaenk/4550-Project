import time
import random
from Question import Question
from server import clients, client_usernames






players = []


class Player:
    def __init__(self, socket, username):
        self.socket = socket
        self.username = username
        self.score = 0


    def update_score(self, points):
        self.score += points


def create_players():
    for client_socket in clients:
        username = client_usernames.get(client_socket)
        players.append(Player(client_socket, username))


def send_question(question):
    for player in players:
        # Send the question
        player.socket.send(f"Question: {question}\n".encode())


def prompt_for_answers():
    for player in players:
        # Prompt each player explicitly after question is sent
        player.socket.send("Your answer: ".encode())


def collect_answers():
    answers_dict = {}
    for player in players:
        try:
            answer = player.socket.recv(1024).decode().strip()
            answers_dict[player.username] = answer
        except:
            answers_dict[player.username] = "No response"
    return answers_dict


def choose_topic():
    with open('topic.txt','r') as f:
        topics = f.readlines()
    return random.choice(topics).strip() #chooses random topics, gets rid of newline


def run_game():
    print("Starting Trivia Game")
    create_players()


    for round_num in range(3):
        topic = choose_topic()
        print(topic)
        question_obj = Question(topic,10)
        question = question_obj.getQuestion()
        correct_answer = question_obj.getAnswer()


        # Step 1: Send the question first
        send_question(question)


        # Step 2: Delay to ensure question delivery
        time.sleep(1)


        # Step 3: Prompt explicitly for answers
        prompt_for_answers()


        # Step 4: Collect answers
        player_answers = collect_answers()


        # Feedback and scoring
        for player in players:
            answer = player_answers.get(player.username, "No response")
            if answer.lower() == correct_answer.lower():
                player.update_score(10)
                response = f"Correct! Your score: {player.score}\n"
            else:
                response = f"Incorrect. Correct answer was '{correct_answer}'. Your score: {player.score}\n"
            player.socket.send(response.encode())


        print(f"Round {round_num + 1} complete.")


    # End game and display final scores
    print("Game over! Final scores:")
    for player in players:
        final_message = f"Final score for {player.username}: {player.score}\n"
        player.socket.send(final_message.encode())
        print(final_message)


if __name__ == "__main__":
    run_game()
