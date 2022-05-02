from flask import Flask, request
from flask import render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac595d158a0b804c36102ec03c7355d5e501bd66f7e0ad2b'

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/written_overview")
def written_overview():
    return render_template("CSC455ProjectProposal.html")


@app.route("/erd_diagram")
def erd_diagram():
    return render_template("logicalERD.html")


@app.route("/logical_schema")
def logical_schema():
    return render_template("logicalSchema.html")

@app.route("/tbl_dgn_rel_data")
def table_design():
    return render_template("tblDgnRelData.html")

@app.route("/supporting_queries")
def supporting_queries():
    
    return render_template('supportingQueries.html')