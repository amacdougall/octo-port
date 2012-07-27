"""
Top-level doc comment.
"""
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import yaml

# load constants from external file for ultra-secret security
constants = yaml.load(open("settings.yaml"))

# CONSTANTS
DEBUG = True
GITHUB_CLIENT_ID = constants["GITHUB_CLIENT_ID"]
GITHUB_CLIENT_SECRET = constants["GITHUB_CLIENT_SECRET"]


# APP CONFIG
app = Flask(__name__)
app.config.from_object(__name__)


# ROUTES
@app.route("/home")
def home():
    return render_template("home.jinja2")


# UTILITY


# USE AWFUL BUT STANDARD-ISSUE PYTHON HACK TO RUN THE SCRIPT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(host="0.0.0.0", port=port)
