from flask import Flask, send_file, request
from main import create_ticket
import shutil
import os
app = Flask(__name__)


@app.route('/get_ticket', methods=['POST'])
def get_ticket():
    create_ticket(request.get_json())

    return send_file("output.png"), 200



if __name__ == '__main__':
    app.run(debug=True, port=8000)