import psycopg2

CREATE_DATABASE_WORKSHOP = """CREATE DATABASE workshop;"""

USER = 'postgres'
PASS = 'coderslab'
HOST = 'localhost'
DATABASE = "workshop"

CREATE_TABLE_USERS = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_pass VARCHAR(80));"""

CREATE_TABLE_MESSAGES = """CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    from_id INT REFERENCES users(id) ON DELETE CASCADE,
    to_id INT REFERENCES users(id) ON DELETE CASCADE,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(255));"""

try:
    with psycopg2.connect(user=USER, password=PASS, host=HOST) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(CREATE_DATABASE_WORKSHOP)
            except psycopg2.errors.DuplicateDatabase as e:
                print("Database 'workshop' already exists.", e)
except psycopg2.OperationalError as e:
    print("Connection Error: ", e)

try:
    with psycopg2.connect(user=USER, password=PASS, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_USERS)
            cur.execute(CREATE_TABLE_MESSAGES)
except psycopg2.OperationalError as e:
    print("Connection Error: ", e)
