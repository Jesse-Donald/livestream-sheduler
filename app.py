import os
import secrets
from flask import Flask, render_template, redirect, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.middleware.proxy_fix import ProxyFix

from getConfig import *
from shedule import *
from getThumb import *
from planningCenter import *
from googleAuth import *

app = Flask(__name__)

# Trust Nginx Proxy Manager headers (including X-Forwarded-Prefix for /stream)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Use a fixed secret key from env so sessions survive restarts and multi-worker setups
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "change-me-in-production-to-a-fixed-random-string"


class NameForm(FlaskForm):
    title = StringField('Stream Title', validators=[DataRequired()])
    name = StringField('Preacher', validators=[DataRequired(), Length(1, 40)])
    submit = SubmitField('Update Preview')


@app.route("/", methods=['GET', 'POST'])
def index():
    data = getConfig()
    form = NameForm()
    if form.validate_on_submit():
        writeConfig('Preacher', form.name.data)
        writeConfig('SermonTitle', form.title.data)
        generateThumb()
        return redirect(os.environ.get(
        "URL_SUBPATH",
        "/"
    ).strip().strip('"').strip("'"))
    else:
        form.name.data = data['Preacher']
        form.title.data = data['SermonTitle']

    return render_template('index.html', data=data, form=form)


@app.route("/createstream")
def generatestream():
    createStream()
    return redirect(os.environ.get(
        "URL_SUBPATH",
        "/"
    ).strip().strip('"').strip("'"))


@app.route("/generateThumb")
def schedule():
    getNames()
    generateThumb()
    return redirect(os.environ.get(
        "URL_SUBPATH",
        "/"
    ).strip().strip('"').strip("'"))



@app.route("/getauthurl")
def authurl():
    # Clicking the button hits /getauthurl and immediately redirects to Google
    auth_url, state, code_verifier = getAuthURL()
    session["oauth_state"] = state
    session["code_verifier"] = code_verifier
    return redirect(auth_url)


@app.route("/auth_return")
def auth_return():
    auth_creds_return(
        request,
        state=session.get("oauth_state"),
        code_verifier=session.get("code_verifier"),
    )
    # Opens the logged-in user's own YouTube Studio
    return redirect("https://studio.youtube.com")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
