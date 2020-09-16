from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user, LoginManager

from database import init_db_command
from userclass import User

from oauthlib.oauth2 import WebApplicationClient

import json
import os
import sqlite3
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import random
import requests
from statistics import mean

GOOGLE_CLIENT_ID = "175654411694-1kps1i1crfj0te22l0afsfadbd5unoqk.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "IpzCigk8RYcFdjJwvy8RgufM"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.urandom(24) or os.environ.get("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id) #this app does not save any user's data, just log in every time...

def get_google_provider_cfg():
	return requests.get(GOOGLE_DISCOVERY_URL).json()    

@app.route('/') # / - default page
def main():
	return render_template("index.html")

@app.route('/login/') # / - hit sign in button and log in
def login():

    g_provider_cfg = get_google_provider_cfg()
    authorization_endpt = g_provider_cfg["authorization_endpoint"]
    uri = client.prepare_request_uri(
        authorization_endpt,
        redirect_uri=request.base_url + "callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(uri)

@app.route("/login/callback")
def callback():
	code = request.args.get("code")
	g_provider_cfg = get_google_provider_cfg()
	t_endpt = g_provider_cfg["token_endpoint"] 
	
	t_url, headers, body = client.prepare_token_request(
		t_endpt,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)
	t_resp = requests.post(
		t_url,
		headers=headers,
		data=body,
		auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
	)
	client.parse_request_body_response(json.dumps(t_resp.json()))
	userinfo_endpt = g_provider_cfg["userinfo_endpoint"]
	uri, headers, body = client.add_token(userinfo_endpt)
	userinfo_resp = requests.get(uri, headers=headers, data=body) 

	if userinfo_resp.json().get("email_verified"):
		unique_id = userinfo_resp.json()["sub"]
		users_email = userinfo_resp.json()["email"]
		picture = userinfo_resp.json()["picture"]
		users_name = userinfo_resp.json()["given_name"]
	else:
		return "Email not verified by Google or not available.", 400 

	user = User(
   		id_=unique_id, profile_pic=picture, name=users_name, email=users_email
	)

	login_user(user)
	if not User.get(unique_id):
		User.create(unique_id, users_name, users_email, picture)

	return redirect(url_for("home")) 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))	   	

@app.route('/home/') # / - logged in
def home():
    return render_template('home.html')

@app.route('/signup/') # / - sign up with a username/password
def signup():
	return render_template("signup.html")

@app.route('/form/') # / - form for adding a room
def form():
	return render_template("form.html")	

@app.route('/submit/',methods=['POST'])
def getValue():
	Room = request.form['Room']
	t1 = request.form['t1']
	t2 = request.form['t2']
	t3 = request.form['t3']
	t4 = request.form['t4']
	t5 = request.form['t5']
	t6 = request.form['t6']
	t7 = request.form['t7']
	t8 = request.form['t8']
	res=[t1,t2,t3,t4,t5,t6,t7,t8]
	tempY = [int(i) for i in res]
	avg = mean(tempY)
	avg = round(avg,1)
	timeX = ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=timeX,y=tempY,mode='markers'))
	fig.update_xaxes(title_text="Time of Day")
	fig.update_yaxes(title_text="Temperature in Fahrenheit")
	fig.show()

	Room_sel = request.form.get("rlist", None)
	if Room_sel != None:
		if Room_sel == "Room1":
			return render_template("home.html",R1=Room_sel)
		elif Room_sel == "Room2":
			return render_template("home.html",R2=Room_sel)
		elif Room_sel == "Room3":
			return render_template("home.html",R3=Room_sel)
		else:
			return render_template("home.html",R4=Room_sel)

	"""
	fig2.add_trace(go.Scatter(x=timeX,y=tempY,mode='markers'))
	
	fig2.update_xaxes(title_text="time")
	fig2.update_yaxes(title_text="humidity")
	cel = [(i-32)/(1.8) for i in tempY]	
	fig2.add_trace(go.Scatter(x=timeX,y=tempY,mode='markers'))
	fig.show()
		
	"""			

@app.route('/simulate/')
def simulate():
	random.seed(a=None, version=2)
	timeX = ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
	fig = make_subplots(rows=2, cols=2)
	colnum = 1
	rownum = 1

	for i in range(4):
		t1 = random.random() * 100
		t2 = random.random() * 100
		t3 = random.random() * 100
		t4 = random.random() * 100
		t5 = random.random() * 100
		t6 = random.random() * 100
		t7 = random.random() * 100
		t8 = random.random() * 100
		res=[t1,t2,t3,t4,t5,t6,t7,t8]
		tempY = [int(j) for j in res]
		avg = mean(tempY)
		avg = round(avg,1)
		if (i == 0):
			rownum = 1
			colnum = 1
		if (i == 1):
			rownum = 1
			colnum = 2
		if (i == 2):
			rownum = 2
			colnum = 1
		if (i == 3):
			rownum = 2
			colnum = 2			
		fig.add_trace(go.Scatter(x=timeX,y=tempY,mode='markers'),row=rownum,col=colnum)


	fig.update_xaxes(title_text="Time of Day")
	fig.update_yaxes(title_text="Temperature in Fahrenheit")
	fig.update_layout(title_text="Simulated Room Data", title_x=0.5)
	fig.show()

	return render_template("home.html")					

if __name__ == "__main__":
	app.run(ssl_context="adhoc", debug="True") 
