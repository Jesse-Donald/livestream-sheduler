from flask import Flask, render_template
from getConfig import *
from shedule import *
from getThumb import *
from googleAuth import *

app = Flask(__name__)

@app.route("/")
def index():
    data=getConfig()
    return render_template('index.html', data=data)

@app.route("/createstream")
def generatestream():
    createStream()
    data=getConfig()
    return render_template('index.html',data=data)

@app.route("/generateThumb")
def schedule():
    generateThumb()
    data=getConfig()
    return render_template('index.html',data=data)

@app.route("/getauthurl")
def authurl():
    authurl = getAuthURL()
    data=getConfig()
    return render_template('index.html',data=data, authurl=authurl)


app.run()