from flask import Flask, render_template, request, redirect, url_for
from flask import session
import pyrebase


app = Flask(__name__, template_folder = "templates", static_folder = "static")

app.config['SECRET_KEY'] = "Your_secret_string"




firebaseConfig = {
 'apiKey': "AIzaSyBVzNwlQu9YJg4gyPH0M33bR-shkBKOUks",
  'authDomain': "y2-project-bed2a.firebaseapp.com",
  'projectId': "y2-project-bed2a",
  'storageBucket': "y2-project-bed2a.appspot.com",
  'messagingSenderId': "644440033641",
  'appId': "1:644440033641:web:9eb678d28a328fca3b55f8",
  'databaseURL':"https://y2-project-bed2a-default-rtdb.europe-west1.firebasedatabase.app/"

}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db =firebase.database()


@app.route("/signup", methods= ['GET', 'POST'])
def sign_up():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		psw = request.form['p']
		userName = request.form['username']
		users={"Email": email, "password": psw, "userName": userName}
		try:
			session['user'] = auth.create_user_with_email_and_password(email, psw)
			session['quotes'] = []
			uid = session['user']['localId']
			db.child("users").child(uid).set(users)

			return redirect(url_for('signin'))
		except Exception as e:
			print(e)
			return render_template("signin.html")

	return render_template("signup.html")
   

@app.route("/sign_in", methods= ['GET', 'POST'])
def signIn():
  error=""
  if request.method == 'POST':
    email = request.form['email']
    psw = request.form['p']
    try:
      session['user'] = auth.sign_in_with_email_and_password(email, psw)
      session['quotes'] = []
      return redirect(url_for('work'))
    except :
      error = "Authentication failed"
      print(error)
      return redirect(url_for('work'))
  else:
    return render_template("signin.html")



@app.route("/", methods= ['GET', 'POST'])
def home():
	return render_template("home.html")


@app.route("/dance", methods= ['GET', 'POST'])
def dance():
	return render_template("dance.html")


@app.route("/workouts", methods= ['GET', 'POST'])
def work():
	return render_template("workout.html")


@app.route("/meals", methods= ['GET', 'POST'])
def meal():
	return render_template("meal.html")



@app.route("/profile", methods= ['GET', 'POST'])
def profile():
    if 'user' in session:
    	uid = session['user']['localId']
    	user_data = db.child("users").child(uid).get().val()
    	return render_template('profilePage.html', user=user_data)

    return render_template('profilePage.html')


@app.route('/update', methods= ['GET', 'POST'])
def update():
	if request.method == 'POST':
		psw = request.form['p']
		userName = request.form['username']
		users={"password": psw, "userName": userName}
		uid = session['user']['localId']
		db.child("users").child(uid).update(users)
		return redirect(url_for('profile'))
	return render_template('update.html')



@app.route('/signout', methods= ['GET', 'POST'])
def signout():
	session.clear()
	return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(debug=True)

