import random
import re
import sqlite3
import string


def is_valid_params_signup(data):
    allowed_params = {"username", "email", "password1", "password2"}
    if len(data) < 4 or not set(data.keys()) <= allowed_params:
        return False
    return True


def is_valid_params_login(data):
    allowed_params = {"username", "password"}
    if len(data) < 2 or not set(data.keys()) <= allowed_params:
        return False
    return True


def is_valid_username(username):
    pattern = r"^[a-zA-Z0-9_]+$"
    return bool(re.match(pattern, username))


def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
    return bool(re.match(pattern, email))


def authentication(username, password):
    result = False
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row is not None:
        if password == row[0]:
            result = True

    c.close()
    conn.close()
    return result


def is_duplicate_username(username):
    result = False
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row is not None:
        result = True

    c.close()
    conn.close()
    return result


def is_duplicate_email(email):
    result = False
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    if row is not None:
        result = True

    c.close()
    conn.close()
    return result


def insert(username, password, email):
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password,email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    c.close()
    conn.close()


def is_valid_params_reset_password(data):
    allowed_params = {"verification_code", "password1", "password2", "email"}
    if len(data) < 3 or not set(data.keys()) <= allowed_params:
        return False
    return True


def email_exist(email):
    result = False
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    if row is not None:
        result = True

    c.close()
    conn.close()
    return result


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


def chenge_password(email, password):
    conn = sqlite3.connect(database="users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (password, email))
    conn.commit()
    c.close()
    conn.close()
