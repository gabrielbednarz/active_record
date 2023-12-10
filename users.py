import argparse
import psycopg2
from clcrypto import check_password, hash_password
import models


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-p", "--password", help="password (min 8 characters)")
    parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
    parser.add_argument("-l", "--list", help="list all users", action="store_true")
    parser.add_argument("-e", "--edit", help="edit user", action="store_true")
    parser.add_argument("-d", "--delete", help="delete user", action="store_true")
    return parser.parse_args()


# Separate logic for database connection and cursor which will
# be passed as an argument to each of CRUD functions below.

def execute_with_db(func, *args):
    try:
        with psycopg2.connect(database="workshop", user="postgres", password="coderslab", host="localhost") as conn:
            with conn.cursor() as cur:
                func(cur, *args)  # CRUD function.
    except psycopg2.OperationalError as err:
        print("Connection Error:", err)


def create_user(cur, username, password):
    if len(password) < 8:
        print("Password is too short. It should have minimum 8 characters.")
    else:
        try:
            hashed_password = hash_password(password)
            user = models.Users(username=username, _hashed_password=hashed_password)
            user.save_to_db(cur)
            print("User created")
        except psycopg2.errors.UniqueViolation as e:
            print("User already exists. ", e)


def list_users(cur):
    for user in models.Users.load_all_users(cur):
        print(user.username)


def edit_user(cur, username, password, new_pass):  # Update password.
    user = models.Users.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("New password too short.")
        else:
            user.set_password(new_pass)
            if user.save_to_db():
                print("Password changed.")
    else:
        print(f"Wrong password to {username}.")


def delete_user(cur, username, password):
    user = models.Users.load_user_by_username(cur, username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user.hashed_password):
        if user.delete():
            print(f"User {username} deleted.")
        else:
            print("The user cannot be deleted.")
    else:
        print("Wrong password.")


if __name__ == '__main__':
    args = parse_args()

    if args.username and args.password and args.edit and args.new_pass:
        execute_with_db(edit_user, args.username, args.password, args.new_pass)
    elif args.username and args.password and args.delete:
        execute_with_db(delete_user, args.username, args.password)
    elif args.username and args.password:
        execute_with_db(create_user, args.username, args.password)
    elif args.list:
        execute_with_db(list_users)
    else:
        print("Invalid arguments. Use -h or --help to see the available options.")
