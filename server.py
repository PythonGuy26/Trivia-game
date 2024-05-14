##############################################################################
                                   # server.py
##############################################################################
import time
import random
import socket
import chatlib

# GLOBALS
users = {"guy": {"password": "guy", "Score": 0, "questions_asked": []},
         "test": {"password": "test", "Score": 0, "questions_asked": []},
         "itamar": {"password": "itapi123", "Score": 0, "questions_asked": []}}
game_questions = {1: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
                  2: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpelier"], "correct": 3},
                  3: {"question": "What is the secret identity of Spider-Man", "answers": ["Peter Parker", "Bruce Wayne", "Peter Quill", "Tony Stark"], "correct": 1},
                  4: {"question": "Where did Spider-Man get his spider powers", "answers": ["Radiation", "Magic", "Bio-engineered serum", "Bitten by a spider"], "correct": 4},
                  5: {"question": "Who kills Uncle Ben in the Spider-Man comics", "answers": ["Doctor Octopus", "Chameleon", "Sandman", "Burglar"], "correct": 4},
                  6: {"question": "How old was Peter Parker when he first became Spider-Man", "answers": ["15", "16", "17", "18"], "correct": 3},
                  7: {"question": "What is the name of Peter Parker's aunt in the Spider-Man movies", "answers": ["Sarah", "May", "Gwen", "Betty"], "correct": 2},
                  8: {"question": "Who played Peter Parker/Spider-Man in the original Spider-Man trilogy", "answers": ["Tobey Maguire", "Andrew Garfield", "Tom Holland", "Michael Keaton"], "correct": 1},
                  9: {"question": "Who is Spider-Man's boss at the Daily Bugle", "answers": ["William Randolph Hearst", "J.Jonah Jameson", "Tony Stark", "Nic Fury"], "correct": 2},
                  10: {"question": "Which villain is NOT in Spider-Man's rogue gallery", "answers": ["Green goblin", "Vulture", "Cell", "Lizard"], "correct": 3},
                  11: {"question": "What year was Spider-Man's first appearance", "answers": ["1970", "1962", "1945", "1994"], "correct": 2},
                  12: {"question": "What is the name of Iron Man’s robotic assistant", "answers": ["Ultron", "Jarvis", "Vision", "Groot"], "correct": 2},
                  13: {"question": "What is the name of Iron Man’s father", "answers": ["Howard Stark", "Ronald Stark", "Harry Stark", "James Stark"], "correct": 1},
                  14: {"question": "What country does Iron Man travel to in the movie Iron Man 3", "answers": ["India", "Japan", "China", "Thailand"], "correct": 3},
                  15: {"question": "What element is used as a power source for Iron Man’s suit", "answers": ["Uranium", "Magnesium", "Platinum", "Palladium"], "correct": 4}}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
#What is the secret identity of Spider-Man?


ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS
def loading_progress():
    x = 0.01
    for i in range(101):
        if x < 0.05:
            x += 0.001
        print("\rStarting up: %d%%" % i, end="", flush=True)
        time.sleep(0.1 - x)


def build_and_send_message(conn, code, data=""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, data)
    conn.send(full_msg.encode())
    print("Server: ", full_msg)


def recv_message_and_parse(conn):
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("Client: ", full_msg)
    return cmd, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Receives: -
    Returns: questions dictionary
    """
    game_questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpelier"],
               "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Receives: -
    Returns: user dictionary
    """
    users = {
        "test":	{"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Receives: -
    Returns: the socket object
    """
    print(r""" _______     _         _        
|__   __|   (_)       (_)       
   | | _ __  _ __   __ _   __ _ 
   | || '__|| |\ \ / /| | / _` |
   | || |   | | \ V / | || (_| |
   |_||_|   |_|  \_/  |_| \__,_|""")
    print("Welcome to Trivia Server!")
    time.sleep(1)
    loading_progress()
    time.sleep(1)
    print("\nServer up and running")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Receives: socket, message error string from called function
    Returns: None
    """
    return build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


# MESSAGE HANDLING
def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    user_data = chatlib.split_data(data, 1)
    if user_data[0] in users:
        if user_data[1] == users[user_data[0]]["password"]:
            logged_users[conn.getpeername()] = user_data[0]
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"])
            return "yes", user_data[0]
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Wrong password")
            return "no"
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Wrong username")
        return "no"


def close_checking(conn, code):
    global logged_users
    if code is None:  # Check if the client has closed the connection
        print(f"Client disconnected abruptly")
        del logged_users[conn.getpeername()]
        conn.close()


def create_random_question(conn, user_name):
    global game_questions
    global users
    random_num = random.randint(1, len(game_questions))
    if random_num in users[user_name]["questions_asked"]:
        if list(range(1, len(game_questions) + 1)) == sorted(users[user_name]["questions_asked"]):
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["no_more_questions"])
            raise
        while random_num in users[user_name]["questions_asked"]:
            random_num = random.randint(1, len(game_questions))
    users[user_name]["questions_asked"].append(random_num)
    current_question = game_questions[random_num]
    section = [s for s in current_question]
    return str(random_num)+"#"+current_question[section[0]]+"?#"+"#".join(current_question[section[1]])


def handle_question_message(conn, user_name):
    question_to_send = create_random_question(conn, user_name)
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["send_question"], question_to_send)


def handle_answer_message(conn, user_name, answer):
    question = game_questions[int(answer.split("#")[0])]
    if int(answer[-1]) == question["correct"]:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer"])
        users[user_name]["Score"] += 5
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer"], question["answers"][question["correct"] -1])


def handle_getscore_message(conn, username):
    global users
    score = users[username]["Score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["score_msg"], score)


def handle_highscore_message(conn):
    global users
    sorted_keys = sorted(users, key=lambda x: users[x]["Score"], reverse=True)
    score_table = ""
    for key in sorted_keys:
        score_table += f"{key} : {users[key]['Score']}\n"
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["high_score_msg"], score_table)


def handle_logout_message(conn):
    """
    Closes the given socket (in later chapters, also remove user from logged_users dictionary)
    Receives: socket
    Returns: None
    """
    global logged_users
    del logged_users[conn.getpeername()]
    conn.close()


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions
    listening_socket = setup_socket()
    while True:
        try:
            (client_socket, client_address) = listening_socket.accept()
            print("new client connected from", client_address)

            login = "no"                       # client authenticate
            while login == "no":
                code, msg = recv_message_and_parse(client_socket)
                login, user_name = handle_login_message(client_socket, msg)
                print(client_socket.getpeername())

            while True:                        # client massage analyse
                code, msg = recv_message_and_parse(client_socket)
                close_checking(client_socket, code)    # check for abruptly disconnecting
                if code == chatlib.PROTOCOL_CLIENT["ask_for_question"]:
                    handle_question_message(client_socket, user_name)
                elif code == chatlib.PROTOCOL_CLIENT["send_answer"]:
                    handle_answer_message(client_socket, user_name, msg)
                elif code == chatlib.PROTOCOL_CLIENT["score_msg"]:
                    handle_getscore_message(client_socket, user_name)
                elif code == chatlib.PROTOCOL_CLIENT["high_score_msg"]:
                    handle_highscore_message(client_socket)
                elif code == chatlib.PROTOCOL_CLIENT["logout_msg"]:
                    handle_logout_message(client_socket)
                    print(f"Client {client_address} disconnected")
                    client_socket.close()
                    break

        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == '__main__':
    main()
