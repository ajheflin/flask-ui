from app import app
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from math import floor
import sys
import os
from resan.resan import ResumeAnalyzer
from resan.pdfreader import PDFReader

resan = ResumeAnalyzer()

pages = ["index", "resan", "rescat"]
readable = ["Home", "Resume Analyzer", "Resume Catalog"]

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSION = {'pdf'}

def allowed_file(filename):
	return filename.split(".")[-1] in ALLOWED_EXTENSION

@app.route("/")
def home():
	return render_template("index.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="index")
@app.route("/index")
def index():
	return home()
@app.route("/resan", methods = ["GET"])
def resumeAnalyzer():
	resname = request.args.get('resume', None)
	if resname != None:
		pdftext = PDFReader(os.path.join(app.config['UPLOAD_FOLDER'], resname)).getText()
		resan.setRole("junior dev")
		resan.analyzeText(pdftext)
		unsorted = resan.getLastSkills()
		sortedSkills = resan.sortedSkills()
		sortedList = [(skill, unsorted[skill]) for skill in sortedSkills]
		mini,maxi=resan.getLastExpRange()

		return render_template("res_detail.html", name=resan.getLastName(),
												  degree=str(resan.getLastDegree()),
												  position=resan.getLastJD(),
												  isMatch=resan.getLastMatch(),
												  skills=sortedList,
												  score=resan.getLastExpScore(),
												  min=mini,
												  max=maxi,
												  pages=enumerate(pages),
												  readable=readable,
												  col_width=floor(8 / len(pages)),
												  selected="resan")
	else:
		return render_template("resan.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="resan")
@app.route("/rescat")
def rescat():
	return render_template("rescat.html", pages=enumerate(pages), readable=readable, col_width=floor(8 / len(pages)), selected="rescat")
@app.route("/upload", methods = ["POST"])
def upload_file():
		if request.method == "POST":
			file = request.files['file']
			if file.filename == '':
				flash("No selected files")
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return redirect("/resan?resume=" + filename)
