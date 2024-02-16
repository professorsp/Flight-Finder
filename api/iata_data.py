import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)




@app.route("/get_airport_data", methods=["GET"])
def process_number():
    con = sqlite3.connect(database="iata_data.db")
    cur = con.cursor()
    try:
        send_json = dict()
        cur.execute(
            f"SELECT * FROM iata_data WHERE iata IN ({",".join([f"'{iata}'" for iata in request.args.get("iatas").split(",")])})")
        rows = cur.fetchall()
        for row in rows:
            send_json[row[0]] = {
                "name": row[1],
                "timezone": row[2],
                "lat": row[3],
                "lon": row[4]
            }

        return jsonify(send_json), 200


    except KeyError as e:
        print(e)
        return jsonify({"error": f"<<{e.__str__().replace("'", "")}>> not found"}), 500


if __name__ == "__main__":
    app.run(debug=True)
