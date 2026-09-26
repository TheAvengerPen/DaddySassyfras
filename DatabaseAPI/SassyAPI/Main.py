from flask import Flask
from Controllers.PersonController import app_user
from Controllers.CommandController import app_commands

app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_commands)

if __name__ == "__main__":
    app.run(debug=True)
