import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'e10adc3949ba59abbe56e057f20f883e'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATA_URI']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
  'connect_args': {
    'ssl': {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
}
db = SQLAlchemy(app)
login = LoginManager(app)
