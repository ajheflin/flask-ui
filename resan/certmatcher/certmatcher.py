'''
Author: AJ Heflin
For Geek Sources, Inc.

Certification Matcher using spaCy

https://spacy.io

Requirements:

1.) pip install spacy
2.) python -m spacy download en_core_web_md


'''
import spacy
import os

from spacy.matcher import Matcher

# BEGIN CLASS DEF
class CertMatcher:
	def __init__(self, posit, resume, certs):
		self.nlp = spacy.load("en_core_web_md")
		if type(resume) == str:
			self.restext = resume
			self.resume = self.nlp(self.restext)
		else:
			self.restext = str(resume)
			self.resume = resume
		self.posit = posit
		self.matcher = Matcher(self.nlp.vocab)
		self.certs = certs
		#self.filename = self.posit.replace(" ", "_") + ".txt"
		# if file exists
		'''if os.path.exists("certmatcher/reqs/" + self.filename):
			self.certs = open("certmatcher/reqs/" + self.filename, "r").read().rstrip().split("\n")
			self.certDocs = list(self.nlp.pipe([cert.split(",")[0] for cert in self.certs]))
			self.certPoints = [cert.split(",")[1] for cert in self.certs]
			self.certDict = {}
			for i, name in enumerate(self.certDocs):
				self.certDict.update({str(name): int(self.certPoints[i])})
			for doc in self.certDocs:
				pattern = [[]]
				for token in doc:
					pattern[0].append({"LOWER": token.text.lower()})
				self.matcher.add(str(doc), pattern)
		#fi
		else:
			raise Exception("CertMatcher: No such file exception.\nFile certmatcher/reqs/{} does not exist".format(self.filename))'''
		self.certDocs = list(self.nlp.pipe(self.certs))
		for cert in self.certDocs:
			pattern = [[]]
			for token in cert:
				pattern[0].append({"LOWER": token.text.lower()})
			self.matcher.add(cert.text, pattern)
		#done
		self.matches = self.matcher(self.resume)
	def getMatches(self):
		certs = []
		for match_id, start, end in self.matches:
			certs.append(str(self.resume[start:end]))
		return certs
# END DEF
if __name__ == "__main__":
	resumeString = ''' 850-524-9998
2731 Blair Stone Rd Tallahassee FL, 32301
Objective
Innovative, detail-oriented FSU graduate seeks entry level programming position.
Passionate about software engineering with 10 years of independent study. Strengths in
problem solving, creative thinking, rapid absorption of new skills, and productivity with
minimal supervision.
Education
Florida State University (GPA: 3.4) Tallahassee, FL
Bachelor of Arts Computer Science -- December 2020
Skills
Software Engineering : designed architecture of over a dozen applications
spanning machine learning, database management, and graphical user interfaces
(GUIs). 3+ years professional experience.
Project Manager : spearheaded development of three (3) successful applications
for a total of 1 year management experience.
Python : Django; Flask; AWS. 3 years experience.
C# : .NET; MVC; Unity. 2 years experience.
JavaScript : React. 1 year experience.
C++ : 3 years experience.
C : 2 years experience.
Java : 1 year experience.
Unix : Bash; Linux. 3 years experience.
CSS : 4 years experience.
HTML : 4 years experience.
SQL : 1 year experience.
Certifications:
AWS Certified Solutions Architect
Projects
Softly Into the Night (solo project)
Modular Entity-Component-System (ECS) architecture
Implemented simple algorithmic solutions to complex problems
Compiled 1000s of lines of documented, maintainable code
More Heat Than Light (contract)
Orchestrated development & implementation of modular architecture as part
of a team in a mock agile development environment
Apollo 11 Interactive Exhibit (contract)
Cooperated with art and programming teams to develop interactive UI '''
	certmatcher = CertMatcher("junior dev", resumeString, ["AWS Certified Solutions Architect"])
	print(certmatcher.getMatches())
