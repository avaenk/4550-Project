import time
import random
import threading
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


def collect_answers_with_timer(timeout=60):
    answers_dict = {}
    lock = threading.Lock()
    responses_received = threading.Event()

    def collect_answers():
        # Collect answers within the timeout window
        for player in players:
            try:
                player.socket.settimeout(timeout) # ensures individual client socket reads respect the 1-minute limit.
                answer = player.socket.recv(1024).decode().strip()
                with lock:
                    answers_dict[player.username] = answer
            except:
                with lock:
                    answers_dict[player.username] = "timed out"
        responses_received.set()

    # Start the collection thread
    collection_thread = threading.Thread(target=collect_answers)
    collection_thread.start()

    # Wait for the timeout
    responses_received.wait(timeout)

    # Fill in any unanswered players with "timed out"
    with lock:
        for player in players:
            if player.username not in answers_dict:
                answers_dict[player.username] = "timed out"

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
        player_answers = collect_answers_with_timer(timeout=60)


        # Feedback and scoring
        for player in players:
            answer = player_answers.get(player.username, "No response")
            if answer.lower() == correct_answer.lower():
                player.update_score(10)
                response = f"Correct! Your score: {player.score}\n"
            elif answer == "timed out":
                response = f"You ran out of time! Your score: {player.score}\n"
            else:
                response = f"Incorrect. Correct answer was '{correct_answer}'. Your score: {player.score}\n"
            player.socket.send(response.encode())


        print(f"Round {round_num + 1} complete.")


    # End game and display final scores
    print("Game over! Final scores:")
    print("""
   ╔════════════════════════════════════════════════════════════╗
   ║                      📰 TRIVIA TIMES 📰                     ║
   ║                  "All the Answers That Fit"                ║
   ╚════════════════════════════════════════════════════════════╝

     🎉 Thanks for Playing! 🎉
     
   ╔════════════════════════════════════╗
   ║         Final Scores               ║
   ╚════════════════════════════════════╝
   """)

    for player in players:
        final_message = f"Final score for {player.username}: {player.score}\n"
        player.socket.send(final_message.encode())
        print(final_message)
       


if __name__ == "__main__":
    run_game()
