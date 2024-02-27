from flask import Flask, request, jsonify
import csv
import re
import pandas as pd
import random
import string


def is_valid_params_login(data):
    allowed_params = {"username", "password"}
    if len(data) < 2 or not set(data.keys()) <= allowed_params:
        return False
    return True


def is_valid_params_signup(data):
    allowed_params = {"username", "email", "password1", "password2"}
    if len(data) < 4 or not set(data.keys()) <= allowed_params:
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
    with open("data.csv", 'r') as f:
        file = csv.DictReader(f)
        for row in file:
            if row["username"] == username and row["password"] == password:
                f.close()
                return True
    f.close()
    return False


def is_duplicate_username(username):
    with open("data.csv", 'r') as f:
        file = csv.DictReader(f)
        for row in file:
            if row["username"] == username:
                f.close()
                return True
    f.close()
    return False


def is_duplicate_email(email):
    with open("data.csv", 'r') as f:
        file = csv.DictReader(f)
        for row in file:
            if row["email"] == email:
                f.close()
                return True
    f.close()
    return False


app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not is_valid_params_signup(data):
            return jsonify({"message": "data invalid"}), 400

        username = data["username"].strip()
        password1 = data["password1"].strip()
        password2 = data["password2"].strip()
        email = data["email"].strip()

        if is_duplicate_username(username):
            return jsonify({"message": "username is duplicate"}), 400

        if not is_valid_username(username):
            return jsonify({"message": "username invalid"}), 400

        if password1 != password2:
            return jsonify({"message": "password do not match"}), 400

        if not is_valid_password(password1):
            return jsonify({"message": "password invalid"}), 400

        if not is_valid_email(email):
            return jsonify({"message": "email invalid"}), 400

        if is_duplicate_email(email):
            return jsonify({"message": "email is duplicate"}), 400

        with open("data.csv", 'a', newline="") as f:
            file = csv.DictWriter(f, fieldnames=["username", "password", "email"])
            file.writerow({"username": username, "password": password1, "email": email})
            f.close()

        return jsonify({'message': 'successfull'}), 200

    except Exception as e:
        return jsonify({"message": "server not respone",
                        "error": f'{e}'}), 500


@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not is_valid_params_login(data):
            return jsonify({"message": "data invalid"}), 400

        username = data["username"].strip()
        password = data["password"].strip()

        if not authentication(username, password):
            return jsonify({"message": "username or password not incorect"}), 400

        return jsonify({"message": "successfull"}), 200

    except Exception as e:
        return jsonify({"message": "server not respone"}), 500


# ============================================================================================================
def is_valid_params_reset_password(data):
    allowed_params = {"verification_code", "password1", "password2", "email"}
    if len(data) < 3 or not set(data.keys()) <= allowed_params:
        return False
    return True


def email_exist(email):
    with open("data.csv", 'r') as file:
        csvData = csv.DictReader(file)
        result = False
        for row in csvData:
            if row["email"] == email:
                result = True
        return result


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


codes = dict()


@app.route("/get_verify_code", methods=["GET"])
def get_verify_code():
    global codes

    email = request.args.get("email").strip()

    if not is_valid_email(email):
        return jsonify({"message": "email invalid"}), 400

    if not email_exist(email):
        return jsonify({"message": "email not exist"}), 400

    verifyCode = generate_verification_code()
    print(f"verify code for {email}: {verifyCode}")
    codes[email] = verifyCode

    return jsonify({"message": "successfull"}), 200


@app.route("/reset_password", methods=["POST"])
def reset_password():
    global codes

    data = request.get_json()

    if not is_valid_params_reset_password(data):
        return jsonify({"message": "data invalid"}), 400

    verification_code = data.get("verification_code").strip()
    password1 = data.get("password1").strip()
    password2 = data.get("password2").strip()
    email = data.get("email").strip()
    if password2 != password1:
        return jsonify({"message": "passwords do not match"}), 400

    if not is_valid_password(password1):
        return jsonify({"message": "password invalid"}), 400

    if not email_exist(email):
        return jsonify({"message": "email not exist"}), 400

    if verification_code != codes.get(email):
        return jsonify({"message": "verification code incorrect"}), 400

    df = pd.read_csv("data.csv")
    condition = (df["email"] == email)
    df.loc[condition, "password"] = password1
    df.to_csv("data.csv", index=False)
    del codes[email]
    print(codes)
    return jsonify({"message": "password changed"})


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
