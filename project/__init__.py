from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "RWD-secret-key"
from project import views