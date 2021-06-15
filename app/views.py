from app import app

@app.route("/")
def index():
	return "Welcome page"
@app.route("/resan")
def resan():
	return "Resume Analyzer"
