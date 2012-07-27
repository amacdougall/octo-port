"""
Top-level doc comment.
"""
import os
import pdb
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.urls import url_decode, url_encode
import yaml

# CONSTANTS
# DEBUG = True
GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]

# APP CONFIG
app = Flask(__name__)
app.config.from_object(__name__)


# ROUTES
@app.route("/")
def root():
    params = {"client_id": GITHUB_CLIENT_ID}
    auth_url = "https://github.com/login/oauth/authorize?{params}"
    return redirect(auth_url.format(params=url_encode(params)))

@app.route("/home")
def home():
    return render_template("home.jinja2")

@app.route("/something")
def something():
    return render_template("something.jinja2")

# UTILITY


# USE AWFUL BUT STANDARD-ISSUE PYTHON HACK TO RUN THE SCRIPT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
