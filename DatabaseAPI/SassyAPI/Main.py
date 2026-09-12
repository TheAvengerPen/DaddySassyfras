from flask import Flask
from Controllers.PersonController import app_user

app = Flask(__name__)
app.register_blueprint(app_user)

if __name__ == "__main__":
    app.run(debug=True)
