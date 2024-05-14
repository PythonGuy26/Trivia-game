import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****
import time
SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def connect():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"connecting to {SERVER_IP} in port {SERVER_PORT}")
    return new_socket


def build_and_send_message(conn, code, data=""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, data)
    conn.send(full_msg.encode())


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
    return cmd, data


def build_send_recv_parse(conn, code, data=""):
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def error_and_exit(error_msg):
    if error_msg == "Bye":
        exit()


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data_to_sent = username+chatlib.DATA_DELIMITER+password
        code, answer = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data_to_sent)
        if code == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in!")
            break
        else:
            print(answer)


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"],"")


def print_question(question):
    question = question.split("#")
    print(f"{question[1]}\n1.  {question[2]}\n2.  {question[3]}\n3.  {question[4]}\n4.  {question[5]}")
    return question[0]


def play_question(conn):
    code, question = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["ask_for_question"])
    if code == chatlib.PROTOCOL_SERVER["no_more_questions"]:
        print("No more questions, game over!")
        exit()
    question_num = print_question(question)
    answer = input("What is your answer: ")
    while answer not in ["1", "2", "3", "4"]:
        answer = input("Invalid selection, try again: ")
    code, message = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer"], question_num+chatlib.DATA_DELIMITER+answer)
    if code == chatlib.PROTOCOL_SERVER["correct_answer"]:
        print("Correct!!!")
    else:
        print("Nope, the answer is ", message)
    

def get_score(conn):
    code, answer = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["score_msg"])
    if code != chatlib.PROTOCOL_SERVER["score_msg"]:
        print("error")
    else:
        print("your score is: ", answer)


def get_highscore(conn):
    code, answer = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["high_score_msg"])
    if code != chatlib.PROTOCOL_SERVER["high_score_msg"]:
        print("error")
    else:
        print(answer)


def get_logged_users(conn):
    code, answer = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["logged_users_msg"])
    print(answer)


def main():
    connection = connect()
    login(connection)
    while True:
        print("""Chose what you want to do\na        Play a trivia question
b        Get my score
c        Get high score
d        Get logged users
q        Quit""")
        answer = input("please enter your choice:  ")
        if answer == "a":
            another_question = "y"
            while another_question.lower() == "y" or another_question.lower() == "yes":
                play_question(connection)
                another_question = input("do you want to play another question? y or n:  ")
        elif answer == "b":
            get_score(connection)
        elif answer == "c":
            get_highscore(connection)
        elif answer == "d":
            get_logged_users(connection)
        elif answer == "q":
            logout(connection)
            time.sleep(3)
            exit()



if __name__ == '__main__':
    main()
