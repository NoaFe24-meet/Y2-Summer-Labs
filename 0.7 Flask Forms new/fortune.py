from flask import Flask, render_template
import random
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/home')
def home():
    return render_template("home_fortune.html")

@app.route('/fortune')
def fortune(): 
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

    forNum= random.randint(0, len(your_fortune)-1)
    return render_template("fortune.html", fortune= your_fortune[forNum])



    
if __name__ == '__main__':
    app.run(debug=True)