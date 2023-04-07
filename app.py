from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
  return "<h3>Hello</h3>"


app.run(host='0.0.0.0', debug=True)