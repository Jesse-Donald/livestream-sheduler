from flask import Flask, render_template, redirect
from getConfig import *
from shedule import *
from getThumb import *
from planningCenter import *
from googleAuth import *
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
csrf = CSRFProtect(app)

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

class NameForm(FlaskForm):
    title = StringField('Stream Title', validators=[DataRequired()])
    name = StringField('Preacher', validators=[DataRequired(), Length(1, 40)])
    submit = SubmitField('Update Preview')

@app.route("/", methods=['GET', 'POST'])
def index():
    data=getConfig()
    form=NameForm()
#    form.name.data = getConfig()['Preacher']
    if form.validate_on_submit():
        name = form.name.data
#        if name.lower() in names:
            # empty the form field
        form.name.data = ""
        writeConfig('Preacher', name)
        writeConfig('SermonTitle', form.title.data)
        generateThumb()
            # redirect the browser to another route and template
        return redirect('/stream')
    else:
        form.name.data = data['Preacher']
        form.title.data = data['SermonTitle']
    if form.is_submitted() and not form.validate():
        return form.data

  #          message = "That actor is not in our database."
    return render_template('index.html', data=data, form=form)

@app.route("/createstream")
def generatestream():
    createStream()
    data=getConfig()
    return redirect('/stream')

@app.route("/generateThumb")
def schedule():
    getNames()
    generateThumb()
    data=getConfig()
    return redirect('/stream')

@app.route("/getauthurl")
def authurl():
    authurl = getAuthURL()
    data = getConfig()
    form=NameForm()
    form.name.data = data['Preacher']
    form.title.data = data['SermonTitle']
    return render_template('index.html', data=data, authurl=authurl, form=form)

@app.route("/auth_return")
def auth_return():
    auth_creds_return()
    return redirect('https://studio.youtube.com/channel/UCAPsJAqTs3y5a1sogz4BVdw/livestreaming/manage')

#app.run()
