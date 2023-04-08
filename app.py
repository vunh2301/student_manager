from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
db_connection_string = "mysql+pymysql://wyalya27czj8kcle0b81:pscale_pw_yc5qfmQ8EQ6k5jLgtrUjvV5njUiCnM8IY6b7tZaLlhC@aws.connect.psdb.cloud/students?charset=utf8mb4"
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }},
                       echo=True)
conn = engine.connect()

# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from models import User

# students = Table(
#   'students',
#   meta,
#   Column('id', Integer, primary_key=True),
#   Column('name', String),
#   Column('gender', String),
#   Column('brithday', String),
#   Column('address', String),
# )
# s = students.select()

# result = conn.execute(s)
# for row in result:
#   print(row)
# db = SQLAlchemy(app)
# login = LoginManager(app)
