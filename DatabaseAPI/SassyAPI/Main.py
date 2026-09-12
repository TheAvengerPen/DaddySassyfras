from flask import Flask, request, jsonify

import PeopleFns
from DBCommunication import DBConnector

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def getUser(user_id):
    output = PeopleFns.get_person_data(user_id)

    if output == -1:
        return "Error running SQl. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    print(jsonify(output))

    return jsonify(output), 204


@app.route("/create-user", methods=["POST"])
def createUser():
    data = request.get_json()
    if data:
        return jsonify(data), 201
    return False, 401

if __name__ == "__main__":
    app.run(debug=True)
