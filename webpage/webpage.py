from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/login/') # / - default page
def login():
	return render_template("templates/index.html")

@app.route('/home/') # / - logged in
def home():
	return render_template("templates/home.html")	

@app.route('/signup/') # / - sign up with a username/password
def signup():
	return render_template("templates/signup.html")		

if __name__ == "__main__":
	app.run() 
