from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
db_connection_string = "mysql+pymysql://01l3qjmdqqa2hzei4es0:pscale_pw_byp2LROxNX1n6Xbo4dDVjjc3cEu9pNQa5iT7rru8VVb@aws.connect.psdb.cloud/students?charset=utf8mb4"
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }},
                       echo=True)
conn = engine.connect()
