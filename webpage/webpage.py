from flask import Flask
from flask import render_template
from statistics import mean
import plotly
import plotly.graph_objects as go 

app = Flask(__name__)


@app.route("/")
def main():
    return (render_template('home.html'))

@app.route('/login/') # / - default page
def login():
	return render_template("index.html")

@app.route('/home/') # / - logged in
def home():
	return render_template("home.html")	

@app.route('/signup/') # / - sign up with a username/password
def signup():
	return render_template("signup.html")		

@app.route('/submit',methods=['POST'])
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
    fig.update_xaxes(title_text="time")
    fig.update_yaxes(title_text="temperature")
    fig.show()
	return('Home.html')
    

if __name__ == "__main__":
	app.run() 
