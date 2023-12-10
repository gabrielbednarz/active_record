from clcrypto import hash_password


class Users:
    def __init__(self, _id=-1, username='', _hashed_password=''):
        self._id = _id
        self.username = username
        self._hashed_password = _hashed_password

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    def save_to_db(self, cursor):
        if self.id == -1:
            sql = """INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id;"""
            cursor.execute(sql, (self.username, self.hashed_password))
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET username = %s, hashed_password = %s WHERE id = %s;"""
            cursor.execute(sql, (self.username, self.hashed_password, self.id))
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = f"""SELECT * FROM users WHERE username = %s;"""
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row:
            return Users(row[0], row[1], row[2])

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """SELECT * FROM users WHERE id = %s;"""
        cursor.execute(sql, (id_,))
        row = cursor.fetchone()
        if row:
            return Users(row[0], row[1], row[2])

    @staticmethod
    def load_all_users(cursor):
        users = []
        cursor.execute("""SELECT * FROM users;""")
        for row in cursor.fetchall():
            users.append(Users(row[0], row[1], row[2]))
        return users

    def delete(self, cursor):
        cursor.execute("""DELETE FROM users WHERE id = %s;""", (self.id,))
        # self._id = -1
        return True


class Messages:
    def __init__(self, _id=-1, from_id=None, to_id=None, creation_date=None, text=''):
        self._id = _id
        self.from_id = from_id
        self.to_id = to_id
        self._creation_date = creation_date
        self.text = text

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages (from_id, to_id, creation_date, text) VALUES (%s, %s, %s, %s) RETURNING id;"""
            cursor.execute(sql, (self.from_id, self.to_id, self.creation_date, self.text))
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE messages SET from_id = %s, to_id = %s, creation_date = %s, text = %s WHERE id = %s;"""
            cursor.execute(sql, (self.from_id, self.to_id, self.creation_date, self.text, self.id))
            return True

    @staticmethod
    def load_all_messages(cursor):
        messages = []
        cursor.execute("""SELECT * FROM messages;""")
        for row in cursor.fetchall():
            messages.append(Messages(row[0], row[1], row[2], row[3], row[4]))
        return messages
