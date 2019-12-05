# -*-coding:Utf-8 -*
from flask import *

# --- calling Flask API ---
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
