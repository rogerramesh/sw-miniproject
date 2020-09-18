# SoftwareMiniProject

Repository for Software Mini Project for Senior Design at Boston University, 2020.

This is a Readme for the "Home Monitor project".  This project is built using Python 3, HTML5, CSS and additionally it uses Python API libraries like Flask, Plotly, OpenSSL, OAuth2.  The project is deployed as a Flask application on AWS Cloud Infrastructure (Ubuntu Linux AMI) and it leverages Single Sign-on (SSO) using OpenID/OAuth2 interfaces with Facebook.

Installation & Components:

1. AWS Cloud Infrastructure (Ubuntu EC2 Instance) running:
   - Python 3
   - Flask (latest)
   - Plotly (latest)
   - OpenSSL (latest)
   - OAuth2 (latest)

2. Domain Name must be registered with a Web registrar

3. Use Route 53 (Manage DNS) to redirect Domain name to EC2 Instance IP address

Usage:

1. To access the Home Monitor App, visit our project please go to https://www.homemonitor.tech/
2. Login using our Facebook user account and password.  You will redirected to the home page of "Home Monitor Application". This application can be accessed using any Web browser.


How it works:
   - User signs on using their Facebook account and is redirected to the Home page
   - User inputs data manually throught the provided HTML forms or can run a simulation based on randomized data generated
   - Web app displays a scatter plot using through the use of the Plotly library of the temperature as time progresses
   - User has option to add up to 4 rooms and provide their temperature data and humidity levels
   - User can also delete the rooms and data they've added 


Luke Staib and Roger Ramesh