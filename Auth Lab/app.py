from flask import Flask, render_template, request, redirect, url_for
from flask import session
import pyrebase


app = Flask(__name__, template_folder = "templates", static_folder = "static")

app.config['SECRET_KEY'] = "Your_secret_string"




firebaseConfig = {
  "apiKey": "AIzaSyCH8MHRTx7Cx8IxncH61Y361iL56EB62JY",
  "authDomain": "auth-lab-132ee.firebaseapp.com",
  "projectId": "auth-lab-132ee",
  "storageBucket": "auth-lab-132ee.appspot.com",
  "messagingSenderId": "982443729658",
  "appId": "1:982443729658:web:1120ed615aed62d9749f43",
  "databaseURL": "https://auth-lab-132ee-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db =firebase.database()

@app.route("/", methods= ['GET', 'POST'])
def sign_up():
    error = ""
    if request.method == 'POST':
      email = request.form['email']
      psw = request.form['p']
      user1 = {'fullname':"",'email':"",'username':""}
      try:
        session['user'] = auth.create_user_with_email_and_password(email, psw)
        session['quotes'] = []
        uid = session['user']['localID']
        db.child('Users').child(uid).set(user1)
        return redirect(url_for('home'))
      except:
        error = "Authentication failed"
        print(e)
        return render_template("error.html")

    return render_template("signup.html")
   



@app.route("/sign_in", methods= ['GET', 'POST'])
def sign_in():
  error=""
  if request.method == 'POST':
    email = request.form['email']
    psw = request.form['p']

    try:
      session['user'] = auth.sign_in_with_email_and_password(email, psw)
      session['quotes'] = []
      return redirect(url_for('home'))
    except :
      error = "Authentication failed"
      print(error)
      return redirect(url_for('home'))
  else:
    return render_template("signin.html")


@app.route('/home', methods = ['GET','POST'])
def home():
  if request.method == 'POST':
    quote = request.form['quote']
    speaker = request.form['speaker']
    session['quotes'][speaker] = quote
    session['speaker'] = speaker
    session.modified = True
    return redirect(url_for('display'))
  return render_template('home.html')
  



@app.route("/thanks", methods=['GET', 'POST'])
def thanks():
    if 'user' not in session:
        return redirect(url_for('sign_in'))
    speaker = session.get('speaker')
    quote = session['quotes'].get(speaker, "")
    return render_template("thanks.html", quote=quote, speaker=speaker)


@app.route("/display", methods=['GET', 'POST'])
def display(quotes):
  quotes = login_session['qoute']
  return render_template("display.html",quotes=quotes)


@app.route("/signout")
def signout():
  return render_template("signin.html")



if __name__ == '__main__':
  app.run(debug=True)

