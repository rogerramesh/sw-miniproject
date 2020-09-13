from flask import Flask
from flask import render_template
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/login/') # / - default page
def login():
	return render_template("index.html")

@app.route('/home/') # / - logged in
def home():
	return render_template("home.html")	

@app.route('/signup/') # / - sign up with a username/password
def signup():
	return render_template("signup.html")		

if __name__ == "__main__":
	app.run() 