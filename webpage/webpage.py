from flask import Flask
from flask import render_template, request, redirect
from statistics import mean
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import random

app = Flask(__name__)

@app.route('/login/') # / default page
def login():
	return render_template("index.html")

@app.route('/home/') # logged in
def home():
    return render_template('home.html')

@app.route('/signup/') # sign up with a username/password? will probably remove this
def signup():
	return render_template("signup.html")

@app.route('/form/') # / form for adding a room
def form():
	return render_template("form.html")	

@app.route('/submit/',methods=['POST']) # / room adding route
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

@app.route('/simulate/') # / simulation route
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
	app.run() 
