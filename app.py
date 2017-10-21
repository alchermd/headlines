from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "no news is good news :)"


if __name__ == "__main__":
    app.run()