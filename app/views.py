from app import app
from flask import render_template
from math import floor
import sys

pages = ["index", "resan", "rescat"]
readable = ["Home", "Resume Analyzer", "Resume Catalog"]

@app.route("/")
def home():
	return render_template("index.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="index")
@app.route("/index/")
def index():
	return home()
@app.route("/resan/")
def resan():
	return render_template("resan.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="resan")
@app.route("/rescat/")
def rescat():
	return render_template("rescat.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="rescat")
