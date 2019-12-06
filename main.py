# -*-coding:Utf-8 -*
from flask import *
from werkzeug.security import *
import modules.functions as func

# --- calling Flask API ---
app = Flask(__name__)

# --- setting constants ---
student_file_path = './data/students.json'
studentDict=func.json_to_dictionary(student_file_path)

@app.route('/secret')
def secret():
    return render_template("secret.html")

@app.route('/escape')
def escape():
    res.set_cookie('escape', value=true, max_age=60*20)
    return render_template("secret.html")

@app.route('/enDeveloppement')
def enDeveloppement():
    return render_template("enDeveloppement.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/inscription')
def inscription():
    return render_template("formulaire.html")


@app.route('/visualisation')
def visualisation():
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

@app.route('/redir_from_secret', methods=['GET', 'POST'])
def redir_from_secret():
    num = request.form['numeroSecret']
    if num == 0:
        if 'escape' in request.cookies:
          return render_template("fincs.html")
        else:
          return render_template("fincs.html")
    else:
        return render_template("secretMissed.html")


@app.route('/redirect_to_index_from_connexion', methods=['GET', 'POST'])
def redir_from_connexion():
    mail = request.form['mail']
    password = request.form['password']
    if password is None or mail == "" or mail is None or password == "":
        return redirect(url_for('connexion_failed'))
    truePassword = func.get_password(studentDict, mail)
    if check_password_hash(truePassword, password):
        res = make_response(redirect(url_for('visualisation')))
        if 'mail' in request.cookies:
          res.set_cookie('mail', '', expires=0)
        res.set_cookie('mail', value=mail, max_age=None)
        return res
    else:
        return redirect(url_for('connexion_failed'))

@app.route('/redirect_to_index_from_formulaire', methods=['GET','POST'])
def redir_from_formulaire():
	mail = request.form['mail']
	dico={
	"name": request.form['name'],
	"surname": request.form['surname'],
	"password": generate_password_hash(request.form['password'], "sha256"),
	"birthDate": request.form['birthDate'],
	"gender": request.form['gender'],
 	"tel": request.form['tel'],
	"nationality": request.form['nationality'],
	"address": {
    	"streetNumber": request.form['streetNumber'],
    	"streetName": request.form['streetName'],
    	"complement": request.form['complement'],
    	"ZIPCode": request.form['ZIPCode'],
    	"city": request.form['city']
	},
	"nStudent": request.form['nStudent'],
	"nSecu": request.form['nSecu'],
	"bacMention": request.form['bacMention'],
	"yearStudies": request.form['yearStudies'],
	"typeStudies": request.form['typeStudies'],
	"earnings": request.form['earnings'],
	"parentEarnings": request.form['parentEarnings']
	}
	studentDict[mail]=dico
	func.dictionary_to_json(student_file_path, studentDict)
	return redirect(url_for('index'))


@app.route('/help')
def aides():
	mail = request.cookies.get('mail')
	if 'mail' not in request.cookies:
		return render_template("index.html")
	mail = request.cookies.get('mail')
	values = func.get_data(studentDict, mail)
	return render_template("help.html")


if __name__ == '__main__':
    app.run()

