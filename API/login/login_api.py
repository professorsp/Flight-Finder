from flask import Flask, request, jsonify

from db import *

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

        insert(username, password1, email)

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

    if not is_valid_password(password1):
        return jsonify({"message": "password invalid"}), 400

    if password2 != password1:
        return jsonify({"message": "passwords do not match"}), 400

    if not email_exist(email):
        return jsonify({"message": "email not exist"}), 400

    if verification_code != codes.get(email):
        return jsonify({"message": "verification code incorrect"}), 400

    chenge_password(email, password1)
    del codes[email]
    print(codes)
    return jsonify({"message": "password changed"})


if __name__ == '__main__':
    app.run(port=80, debug=True)
