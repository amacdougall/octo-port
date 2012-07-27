"""
Top-level doc comment.
"""
import os
import StringIO
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_file
from werkzeug.urls import url_decode, url_encode
import yaml

# CONSTANTS
# DEBUG = True
GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
# Field names used in CSV output rows
FIELDNAMES = [
    "created_at",    # created_at [formatted?]
    "updated_at",    # updated_at
    "closed_at",     # closed_at [formatted?]
    "created_by",    # user
    "assignee",      # assignee.login
    "number",        # number
    "html_url",      # html_url
    "pull_request",  # pull_request.html_url
    "state",         # state
    "labels",        # ", ".join([name for label in labels])
    "milestone",     # milestone.title
    "comments",      # comments [it's just a count, which is fine]
    "title",         # title
    "body",          # body
]

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

@app.route("/gimme-csv", methods=['POST', 'GET'])
def build():
    # just get the issues CSV, why not
    input_file = open("issues.csv")
    csv = input_file.read()
    input_file.close()

    output_file = StringIO.StringIO()
    output_file.write(csv)
    output_file.seek(0)
    return send_file(output_file,
                     attachment_filename="issues.csv",
                     as_attachment=True)

# UTILITY
def build_csv(issues, filename):
    """
    Converts the supplied issues to CSV, saving them under the supplied
    filename. Accepts a list of issue dicts as given by the Github API.
    """

    output_file = open(filename, "w")
    for issue in issues:
        csv_writer.writerow(issue_to_row(issue))
    output_file.close()

def issue_to_row(issue):
    """
    Converts an issue dictionary from JSON into a one-dimensional dictionary
    suitable for CSV writing.
    """

    row = {}
    row["created_at"] = issue["created_at"]
    row["updated_at"] = issue["updated_at"]
    row["closed_at"] = issue["closed_at"]
    row["created_by"] = issue["user"]["login"]
    if issue["assignee"]:
        row["assignee"] = issue["assignee"]["login"]
    row["number"] = issue["number"]
    row["html_url"] = issue["html_url"]
    if issue["pull_request"]:
        row["pull_request"] = issue["pull_request"]["html_url"]
    row["state"] = issue["state"]
    row["labels"] = ", ".join([label["name"] for label in issue["labels"]])
    if issue["milestone"]:
        row["milestone"] = issue["milestone"]["title"]
    row["comments"] = issue["comments"]
    row["title"] = issue["title"]
    row["body"] = issue["body"]

    # encode as UTF-8, since CSV must be ASCII; clients will decode
    for key, value in row.items():
        if hasattr(value, "encode"): # only encode encodables!
            row[key] = value.encode("utf-8")

    return row

# USE AWFUL BUT STANDARD-ISSUE PYTHON HACK TO RUN THE SCRIPT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
