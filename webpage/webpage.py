import flask
import os
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import random
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from statistics import mean

#update with AWS website!
siteURL = "https://127.0.0.1:5000"

#Facebook
facebookAuthURL = "https://www.facebook.com/dialog/oauth"
facebookTokenURL = "https://graph.facebook.com/oauth/access_token"

facebookClientID = '335103650875723'
facebookSecretID = '2292cf39c6921bff84289c91c711c493'
facebookScope = ['email']

#Google
googleAuthURL = "https://accounts.google.com/o/oauth2/v2/auth"
googleTokenURL = "https://www.googleapis.com/oauth2/v4/token"
googleRefreshURL = googleTokenURL

googleClientID = '175654411694-1kps1i1crfj0te22l0afsfadbd5unoqk.apps.googleusercontent.com'
googleSecretID = 'IpzCigk8RYcFdjJwvy8RgufM'

googleScope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

#Start app
app = flask.Flask(__name__)
app.secret_key = googleSecretID #google needs this...

@app.route('/') # / - default page
def main():
	return flask.render_template("index.html")

@app.route('/login-fb') #login with fb
def login():
    fb = requests_oauthlib.OAuth2Session(
        facebookClientID, redirect_uri=siteURL + "/callback-fb", scope=facebookScope
    )
    authURL, _ = fb.authorization_url(facebookAuthURL)

    return flask.redirect(authURL)

@app.route("/callback-fb") #login routing with fb
def callback():
    fb = requests_oauthlib.OAuth2Session(
        facebookClientID, scope=facebookScope, redirect_uri=siteURL + "/callback-fb"
    )
    #compliance fix
    fb = facebook_compliance_fix(fb)

    fb.fetch_token(
        facebookTokenURL,
        client_secret=facebookSecretID,
        authorization_response=flask.request.url,
    )

    #get user data
    fbUserData = fb.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    #show user they're logged in
    email = fbUserData["email"]
    name = fbUserData["name"]
    pic = fbUserData.get("picture", {}).get("data", {}).get("url")

    return f"""
	Logged into Facebook as: <br><br>
	Email: {email} <br>
	Name: {name} <br>
	Profile Picture: <img src="{pic}"> <br><br>
	Click the home button to proceed:
	<a href="/home">Home</a>
	"""

@app.route('/login-google') #login with google
def logingoogle():
    google = requests_oauthlib.OAuth2Session(
        googleClientID, redirect_uri=siteURL + "/callback-google", scope=googleScope
    )
    authURL, gState = google.authorization_url(googleAuthURL,
		access_type="offline", prompt="select_account")

    flask.session['oauth_state'] = gState
    return flask.redirect(authURL)

@app.route('/callback-google', methods=["GET"]) #login routing with google
def callbackgoogle():
	google = requests_oauthlib.OAuth2Session(
		googleClientID, redirect_uri=siteURL + "/callback-google", state=flask.session['oauth_state']
	)

	tokenGoogle = google.fetch_token(googleTokenURL, client_secret=googleSecretID, authorization_response=flask.request.url)

	flask.session['oauth_token'] = tokenGoogle
	
	google = requests_oauthlib.OAuth2Session(
		googleClientID, token=flask.session['oauth_token']
	)
	googleUserData = google.get(
		"https://www.googleapis.com/oauth2/v1/userinfo"
	).json()

	email = googleUserData["email"]
	name = googleUserData["name"]

	print(googleUserData)

	return f"""
	Logged into Google as: <br><br>
	Email: {email} <br>
	Name: {name} <br><br>
	Click the home button to proceed:
	<a href="/home">Home</a>
	"""

@app.route("/logout")
def logout():
    return flask.redirect("/")	   	

@app.route('/home/') # / - logged in
def home():
    return flask.render_template('home.html')

@app.route('/add-simulate/') # / - form for adding a room
def form():
	return flask.render_template('form.html')

@app.route('/remove/') # / - logged in
def removeform():
    return flask.render_template('removeform.html')		

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
			return flask.render_template("home.html",R1=Room_sel)
		elif Room_sel == "Room2":
			return flask.render_template("home.html",R2=Room_sel)
		elif Room_sel == "Room3":
			return flask.render_template("home.html",R3=Room_sel)
		else:
			return flask.render_template("home.html",R4=Room_sel)

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

	return flask.render_template("home.html")					

if __name__ == "__main__":
	app.run(ssl_context="adhoc", debug="True") 
