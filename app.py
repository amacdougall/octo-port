"""
Top-level doc comment.
"""
import os
import pdb
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.urls import url_decode, url_encode
import yaml

# load constants from external file for ultra-secret security
constants = yaml.load(open("settings.yaml"))

# CONSTANTS
# DEBUG = True
GITHUB_CLIENT_ID = constants['GITHUB_CLIENT_ID']

# APP CONFIG
app = Flask(__name__)
app.config.from_object(__name__)


# ROUTES
@app.route("/")
def home():
    params = {
            'client_id': GITHUB_CLIENT_ID,
        }
    return redirect('https://github.com/login/oauth/authorize?' +
                    url_encode(params))

@app.route("/auth/<service>/callback", methods=["GET", "POST"])
def  callback(service):
    return render_template("home.jinja2")

# UTILITY


# USE AWFUL BUT STANDARD-ISSUE PYTHON HACK TO RUN THE SCRIPT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
