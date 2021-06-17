'''
Author: AJ Heflin
For Geek Sources, Inc.

Skill/Experience Matcher using spaCy

http://spacy.io

Requirements:

1.) pip install spacy
2.) python -m spacy download en_core_web_md

'''
import spacy

from spacy.matcher import Matcher

# BEGIN CLASS DEFINITION
class SkillMatcher:
	def __init__(self, resume):
		self.nlp = spacy.load("en_core_web_md")
		if type(resume) == spacy.tokens.doc.Doc:
			self.restext = str(resume)
			self.resume = resume
		elif type(resume) == str:
			self.restext = resume
			self.resume = self.nlp(self.restext)
		self.matcher = Matcher(self.nlp.vocab)
		self.skills = open("resan/skillmatcher/skills.txt", "r").read().rstrip().split(",")
		skilldocs = list(self.nlp.pipe(self.skills))
		# parse skills
		for skilldoc in skilldocs:
			skilltmp = str(skilldoc)
			pattern = [[]]
			for token in skilldoc:
				if token.pos_ == "VERB":
					token.pos_ = "PROPN"
				#pattern[0].append({"POS": token.pos_, "LOWER": token.text.lower()})
				if len(skilldoc) == 1:
					pattern[0].append({"LOWER": token.text.lower(), "POS": token.pos_})
				else:
					pattern[0].append({"LOWER": token.text.lower()})
			self.matcher.add(skilltmp, pattern)
		self.matches = self.matcher(self.resume)
	def getMatches(self):
		return list(set([self.resume[start:end].text.lower() for match_id, start, end in self.matches]))
	def numMatches(self):
		return len(self.getMatches())
	# uses skills to get related experiences
	def getExperience(self):
		experiences = {}
		self.resLines = self.restext.split("\n")
		self.docLines = list(self.nlp.pipe(self.resLines))
		for doc in self.docLines:
			matches = self.matcher(doc)
			pattern = [[{"IS_DIGIT": True}, {"OP": "?"}, {"LEMMA": "year"}, {"LOWER": "of", "OP": "?"}, {"LOWER": "experience", "OP": "?"}], [{"LEMMA": "year"}, {"LOWER": "of", "OP": "?"}, {"LOWER": "experience", "OP": "?"}, {"OP": "?"}, {"IS_DIGIT": True}, {"OP": "?"}]]
			lstart = -1
			lend = -1
			#if match is found
			if len(matches) > 0:
				matcher = Matcher(self.nlp.vocab)
				matcher.add("Experience", pattern)
				expmatches = matcher(doc)
				longestmatch = -1
				if len(expmatches) > 0:
					for match_id, start, end in expmatches:
						if end - start > longestmatch:
							longestmatch = end - start
							lstart = start
							lend = end
				exp = -1
				languages = []
				for match_id, start, end in matches:
					lang = str(doc[start:end])
					for langu in self.skills:
						if langu.lower() == lang:
							lang = langu
							break
					languages.append(lang)
				if lstart == -1:
					exp = 0
				else:
					yrmatcher = Matcher(self.nlp.vocab)
					yrmatcher.add("Number", [[{"IS_DIGIT": True}]])
					yrmatches = yrmatcher(doc)
					match_id,start,end = yrmatches[0]
					exp = int(str(doc[start:end]))
				for lang in languages:
					experiences.update({lang: exp})
			#fi
		return experiences
# END CLASS DEFINITION
