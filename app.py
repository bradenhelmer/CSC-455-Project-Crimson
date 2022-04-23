from flask import Flask
from flask import render_template



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/written_overview")
def written_overview():
    return render_template("CSC455ProjectProposal.html")

@app.route("/erd_diagram")
def erd_diagram():
    return render_template("logicalERD.html")

