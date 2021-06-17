import spacy

from spacy.matcher import Matcher

class SkillMatcher:
	def __init__(self, resume):
		self.restext = resume
		self.nlp = spacy.load("en_core_web_md")
		self.resume = self.nlp(self.restext)
		self.matcher = Matcher(self.nlp.vocab)
		self.skills = open("skillmatcher/skills.txt", "r").read().rstrip().split(",")
		for skill in self.skills:
			skilltmp = skill
			skilldoc = self.nlp(skill)
			pattern = [[]]
			for token in skilldoc:
				if token.pos_ == "VERB":
					token.pos_ = "PROPN"
				pattern[0].append({"POS": token.pos_, "LOWER": token.text.lower()})
				#pattern[0].append({"LOWER": token.text.lower()})
			print(pattern)
			self.matcher.add(skilltmp, pattern)
		self.matches = self.matcher(self.resume)
	def getMatches(self):
		return list(set([self.resume[start:end].text.lower() for match_id, start, end in self.matches]))
	def numMatches(self):
		return len(self.getMatches())
	def getExperience(self):
		experiences = {}
		self.resLines = self.restext.split("\n")
		self.docLines = []
		for line in self.resLines:
			self.docLines.append(self.nlp(line))
		for doc in self.docLines:
			for token in doc:
				print(token.text,": ", token.pos_, sep="")
			matches = self.matcher(doc)
			pattern = [[{"IS_DIGIT": True}, {"LEMMA": "year"}, {"LOWER": "of", "OP": "?"}, {"LOWER": "experience", "OP": "?"}], [{"LEMMA": "year"}, {"LOWER": "of", "OP": "?"}, {"LOWER": "experience", "OP": "?"}, {"OP": "?"}, {"IS_DIGIT": True}]]
			lstart = -1
			lend = -1
			if len(matches) > 0:
				matcher = Matcher(self.nlp.vocab)
				matcher.add("Experience", pattern)
				expmatches = matcher(doc)
				longestmatch = -1;
				if len(expmatches) > 0:
					for match_id, start, end in expmatches:
						if end - start > longestmatch:
							longestmatch = end - start
							lstart = start
							lend = end
				exp = -1
				languages = []
				for match_id, start, end in matches:
					languages.append(str(doc[start:end]))
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
		return experiences
