# -*-coding:Utf-8 -*
from flask import *
from werkzeug.security import *
import modules.functions as func

# --- calling Flask API ---
app = Flask(__name__)

# --- setting constants ---
student_file_path = './data/students.json'
studentDict=func.json_to_dictionary(student_file_path)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/inscription')
def inscription():
    return render_template("formulaire.html")


@app.route('/visualisation')
def visualisation():
    mail = request.cookies.get('mail')
    if 'mail' not in request.cookies:
        return render_template("index.html")
    else:
       mail = request.cookies.get('mail')
       values = func.get_data(studentDict, mail)
       return render_template("visualisation.html", values = values, mail = mail)


@app.route('/connexion')
def connexion():
    return render_template("connexion.html")


@app.route('/connexion_failed')
def connexion_failed():
    return render_template("connexion_failed.html")


@app.route('/redirect_to_index_from_connexion', methods=['GET', 'POST'])
def redir_from_connexion():
    mail = request.form['mail']
    password = request.form['password']
    if password is None or mail == "":
        return redirect(url_for('connexion_failed'))
    truePassword = func.get_password(studentDict, mail)
    if check_password_hash(truePassword, password):
        res = make_response(redirect(url_for('visualisation')))
        res.set_cookie('mail', value=mail, max_age=None)
        return res
    else:
        return redirect(url_for('connexion_failed'))


if __name__ == '__main__':
    app.run()
