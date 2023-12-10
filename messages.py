import argparse
import psycopg2
from clcrypto import check_password
import models


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-t", "--to", help="recipient username")
    parser.add_argument("-s", "--send", help="message content")
    parser.add_argument("-l", "--list", help="list all messages", action="store_true")
    return parser.parse_args()


def execute_with_db(func, *args):
    try:
        with psycopg2.connect(database="workshop", user="postgres", password="coderslab", host="localhost") as conn:
            with conn.cursor() as cur:
                func(cur, *args)
    except psycopg2.OperationalError as e:
        print("Connection Error:", e)


def list_user_messages(cur, username, password):  # List all messages to the certain recipient.
    get_user = models.Users.load_user_by_username(cur, username)
    if not get_user:
        print(f"{username} does not exist.")
    elif check_password(password, get_user.hashed_password):
        to_id_user_messages = [message for message in models.Messages.load_all_messages(cur)
                               if message.to_id == get_user.id]
        print(f"Listing all messages to the recipient {get_user.username} of id {get_user.id}...")
        for i in to_id_user_messages:
            sender = models.Users.load_user_by_id(cur, i.from_id).username
            print("*" * 20)
            print(f"Message id: {i.id}, message date: {i.creation_date}.")
            print(f"Message content: {i.text}.\n")
            print(f"Sent from {sender}")
            print("*" * 20)
    else:
        print(f"The password you provided isn't correct ({username}).")


def send_message(cur, username_sender, password, recipient, message):
    if not (get_sender := models.Users.load_user_by_username(cur, username_sender)):
        print(f"Sender {username_sender} does not exist.")
        return
    if not (get_recipient := models.Users.load_user_by_username(cur, recipient)):
        print(f"Recipient {recipient} does not exist.")
        return
    if check_password(password, get_sender.hashed_password):
        if len(message) < 255:
            message_instance = models.Messages(from_id=get_sender.id, to_id=get_recipient.id, text=message)
            if message_instance.save_to_db(cur):
                print(f"Sent message from {username_sender} to {recipient}.")
        else:
            print("Your message should be less than 255 characters.")
    else:
        print(f"Wrong password to {username_sender}.")


if __name__ == "__main__":
    args = parse_args()
    if args.username and args.password and args.list:
        execute_with_db(list_user_messages, args.username, args.password)
    elif args.username and args.password and args.to and args.send:
        execute_with_db(send_message, args.username, args.password, args.to, args.send)
    else:
        print("Invalid arguments. Use -h or --help to see the available options.")
