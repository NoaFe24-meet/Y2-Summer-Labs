from flask import Flask, render_template, url_for, redirect, request
from flask import session as login_session
import random
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "Your_secret_string"

@app.route('/home', methods= ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home_fortune.html")
    else:
        birth=request.form["birth"]
        return redirect(url_for("fortune", date=birth))

@app.route('/fortune/<date>')
def fortune(date): 
    your_fortune=[
"An exciting opportunity will come your way soon.",
"Your hard work will pay off in unexpected ways.",
"A journey of a thousand miles begins with a single step.",
"Good things come to those who wait.",
"You will make a new friend who will become very important to you.",
"Unexpected financial gains are coming your way.",
"Trust your instincts; they will guide you well.",
"Love is just around the corner; keep your heart open.",
"You will travel to a place you've always wanted to visit.",
"A pleasant surprise is in store for you today."]

    len_date=len(date)   
    forNum= random.randint(0, len(date))
    if len_date < 10:
     return render_template("fortune.html", fortune= your_fortune[forNum], date_html=date)
    else:
        return render_template("if.html")





    
if __name__ == '__main__':
    app.run(debug=True)