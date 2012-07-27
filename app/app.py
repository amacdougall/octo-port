"""
Top-level doc comment.
"""
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# CONSTANTS
DEBUG = True


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
