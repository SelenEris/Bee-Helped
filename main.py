# -*-coding:Utf-8 -*
from flask import *

# --- calling Flask API ---
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/visualisation')
def visualisation():
    return render_template("visualisation.html")


if __name__ == '__main__':
    app.run()
