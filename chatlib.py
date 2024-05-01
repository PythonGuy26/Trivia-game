# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {"login_msg": "LOGIN",
                   "logout_msg": "LOGOUT",
                   "score_msg": "MY_SCORE",
                   "high_score_msg": "HIGHSCORE",
                   "ask_for_question": "GET_QUESTION",
                   "send_answer": "SEND_ANSWER",
                   "logged_users_msg": "LOGGED"

                   }  # Add more commands if needed


PROTOCOL_SERVER = {"login_ok_msg": "LOGIN_OK",
                   "login_failed_msg": "ERROR",
                   "score_msg": "YOUR_SCORE",
                   "high_score_msg": "ALL_SCORE",
                   "send_question": "YOUR_QUESTION",
                   "correct_answer": "CORRECT_ANSWER",
                   "wrong_answer": "WRONG_ANSWER",
                   "logged_user_msg": "LOGGED_ANSWER",
                   "no_more_questions": "NO_QUESTIONS"
                   }  # Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occurred
    """
    cnd_part = cmd.ljust(CMD_FIELD_LENGTH)
    if len(cnd_part) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
        return None
    if len(data) < 10:
        length_part = "000"+str(len(data))
    elif 100 > len(data) >= 10:
        length_part = "00" + str(len(data))
    elif 1000 > len(data) >= 100:
        length_part = "0" + str(len(data))
    else:
        length_part = str(len(data))
    msg_fields = [cnd_part, length_part, data]
    full_msg = DELIMITER.join(msg_fields)
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    try:
        data_fields = data.split("|")
        cmd = data_fields[0]
        msg = data_fields[2]
        if not data_fields[1].isdigit() or int(data_fields[1]) < 0:
            raise IndexError
        return cmd.strip(), msg
    except IndexError:
        cmd, msg = None, None
        return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """
    if msg.count("#") == expected_fields:
        return msg.split("#")
    else:
        return [None]


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    return "#".join(msg_fields)