'''
Company: Geek Sources, Inc.

resan.py: RESume ANalysis

'''

import spacy

from resan.jtest import Test
from resan.skillmatcher.skillmatcher import SkillMatcher
from resan.certmatcher.certmatcher import CertMatcher

##import data # TODO

# ~~~~~~~~~~~~~~~~~~~~~~~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~ #

REQUIRED = True
NOTREQ = False

MINIMUM_EXP = 2

QUALITIES = {
    'master'        :1,
    'professional'  :1,
    'best'          :1,
    'highest'       :1,
    'wonderful'     :1,
    'superior'      :1,
    'perfect'       :1, # what kind of narcissistic jerk would write that on their resume?
    'excellent'     :0.9,
    'expert'        :0.9,
    'adept'         :0.8,
    'proficient'    :0.8,
    'fluent'        :0.8,
    'great'         :0.8,
    'considerable'  :0.8,
    'confident'     :0.8,
    'strong'        :0.7,
    'keen'          :0.6,
    'competent'     :0.5,
    'fair'          :0.5,
    'sufficient'    :0.4,
    'ordinary'      :0.4,
    'moderate'      :0.4,
    'mediocre'      :0.4,
    'skilled'       :0.4,
    'apprentice'    :0.2,
    'little'        :0.2,
    'some'          :0.2,
    'poor'          :0.1,
    'weak'          :0.1,
    }

# degrees
DEGTYP_NULL     = "NULL"
DEGTYP_IT       = "IT degree"
DEGTYP_NONIT    = "Non-IT degree"

DEGREE_NULL     = "NULL"            # no relevant degree
DEGREE_HS       = "High-school"     # Associate's
DEGREE_TECHNICAL= "Vocational"      # skilled labor
DEGREE_AA       = "AA-degree"       # Associate's
DEGREE_BA       = "BA-degree"       # Bachelor of Arts
DEGREE_BS       = "BS-degree"       # Bachelor of Science
DEGREE_MASTERS  = "Masters-degree"  # Master's
DEGREE_PHD      = "PhD-degree"      # Ph.D.

DEGREES={
DEGREE_NULL     :"None found",
DEGREE_HS       :"High School Diploma",
DEGREE_TECHNICAL:"Vocational",
DEGREE_AA       :"Associate of Arts",
DEGREE_BA       :"Bachelor of Arts",
DEGREE_BS       :"Bachelor of Science",
DEGREE_MASTERS  :"Masters",
DEGREE_PHD      :"Ph.D.",
    }

# degree fields
FIELDS = {
    "Computer Criminology" : DEGTYP_IT,
    "Computer Science" : DEGTYP_IT,
    "Computer Engineering" : DEGTYP_IT,
    "Computer Information Systems" : DEGTYP_IT,
    "Computer Programming" : DEGTYP_IT,
    "Computer Software & Applications" : DEGTYP_IT,
    "Computer Systems Analysis" : DEGTYP_IT,
    "Computer Systems Networking" : DEGTYP_IT,
    "Data Processing" : DEGTYP_IT,
    "Engineering Technology" : DEGTYP_IT,
    "Information Science" : DEGTYP_IT,
    "Information Systems" : DEGTYP_IT,
    "Information Technology" : DEGTYP_IT,
    "Software Engineering" : DEGTYP_IT,
}

# spaCy Matcher patterns
PATTERNS = {
    "AA-degree": [
        [{"LOWER": "associate"}, {"LOWER": "of"}, {"LOWER": "arts"}],
        [{"LOWER": "associate"}, {"LOWER": "degree"}],
        [{"LOWER": "associates"}, {"LOWER": "degree"}],
        [{"LOWER": "associate's"}, {"LOWER": "degree"}],
        [{"LOWER": "a.a."},],
    ],
    "BA-degree": [
        [{"LOWER": "bachelor"}, {"LOWER": "of"}, {"LOWER": "arts"}],
        [{"LOWER": "bachelor"}, {"LOWER": "degree"}],
        [{"LOWER": "bachelors"}, {"LOWER": "degree"}],
        [{"LOWER": "bachelor's"}, {"LOWER": "degree"}],
        [{"LOWER": "b.a."},],
    ],
    "BS-degree": [
        [{"LOWER": "bachelor"}, {"LOWER": "of"}, {"LOWER": "science"}],
        [{"LOWER": "b.s."},]
    ],
    "Masters-degree": [
        [{"LOWER": "master's"}, {"LOWER": "degree"}],
        [{"LOWER": "masters"}, {"LOWER": "degree"}],
        [{"LOWER": "master's"}],
        [{"LOWER": "masters"}],
        [{"LOWER": "ma"},],
        [{"LOWER": "m.a."},],
        [{"LOWER": "a.m."},],
        [{"LOWER": "mphil"},],
        [{"LOWER": "m.phil."},],
        [{"LOWER": "msc"},],
        [{"LOWER": "m.s."},],
        [{"LOWER": "sm"},],
        [{"LOWER": "mba"},],
        [{"LOWER": "m.b.a."},],
        [{"LOWER": "llm"},],
        [{"LOWER": "ll.m."},],
        [{"LOWER": "masc"},],
        [{"LOWER": "mchem"},],
        [{"LOWER": "meng"},],
        [{"LOWER": "mmath"},],
        [{"LOWER": "mpharm"},],
        [{"LOWER": "mphys"},],
        [{"LOWER": "mpsych"},],
        [{"LOWER": "msci"},],
    ],
    "PhD-degree": [
        [{"LOWER": "doctor"}, {"LOWER": "of"}, {"LOWER": "philosophy"}],
        [{"LOWER": "ph.d."},],
        [{"LOWER": "dphil"},],
        [{"LOWER": "d.phil."},],
    ],
}


# logic

# skills
SKILL_NONE      = 0
SKILL_JAVA      = 1     # developer
SKILL_PYTHON    = 2
SKILL_AWS       = 101
SKILL_JIRA      = 201
SKILL_AGILE     = 301   # general Agile including SCRUM
SKILL_SCRUM     = 302   # specific
SKILL_IT        = 401   # general IT skill that doesn't fit other category

SKILLS={
SKILL_JAVA      : ("Java",),
SKILL_PYTHON    : ("Python",),
SKILL_AWS       : ("AWS",),
SKILL_JIRA      : ("Jira",),
SKILL_AGILE     : ("Agile",),
SKILL_SCRUM     : ("SCRUM",),
SKILL_IT        : ("IT",),
}

# certifications

# groups of certifications
CERT_SUITE_JAVA_FULLSTACK   = 1
CERT_SUITE_AWS              = 2

CERTIFICATIONS={
    CERT_SUITE_JAVA_FULLSTACK   : {
        "name" : "Full stack Java developer suite",
        "certs": {
            "" : (REQUIRED, 0,),
        },
    },
    CERT_SUITE_AWS   : {
        "name" : "AWS suite",
        "certs": {
            "AWS Certified Cloud Practitioner" : (NOTREQ, 10,),
            "AWS Certified Solutions Architect Associate" : (NOTREQ, 10,),
            "AWS Certified SysOps Administrator Associate" : (NOTREQ, 10,),
            "AWS Certified Developer Associate" : (NOTREQ, 10,),
            "AWS Certified Solutions Architect Professional" : (NOTREQ, 50,),
            "AWS Certified DevOps Engineer Professional" : (NOTREQ, 50,),
            "AWS Certified Advanced Networking Specialty" : (NOTREQ, 20,),
            "AWS Certified Data Analytics Specialty" : (NOTREQ, 20,),
            "AWS Certified Database Specialty" : (NOTREQ, 20,),
            "AWS Certified Machine Learning Specialty" : (NOTREQ, 20,),
            "AWS Certified Security Specialty" : (NOTREQ, 20,),
        },
    },
##    "AWS professional" : (),
##    "AWS associate" : (),
##    "scrum" : (),
##    "Microsoft" : (),
##    "Oracle" : (),
##    "IT" : (),
##    "other" : (),
}

# job description data
POINTS={

    # Structure:
##        "job role identifier" : {
##            "range" : (low,high,),    # we're looking for someone with a score
                                    # that's somewhere between these values.
    # Note: Ranges should maybe be lenient to account for any mistakes
    # in the analyzer.
##            "experience" : score, # value of 1 year experience
##            "IT degree" : # pick the HIGHEST level degree that's in
                        # an information technology major.
##            "non-IT degree" : # pick the HIGHEST level degree that's
                            # not an information technology major.
##            "certifications" : dict, # each cert class has a specific score

    # Scoring system:
    # Grammar Score * (Experience Score + Degree Score + Certification Score)

    # Experience Score:
    # this is scored by determing the number of years of development
    # experience. Years are not cumulative and the highest skill value
    # is the one chosen for calculation; a resume with 4 years Java
    # experience and 3 years Python experience has exactly 4 years
    # experience for the purpose of this calculation.
    # Score = years * multiplier

    # Degree Score:
    # when scoring degrees, multiple scores are calculated in the case where
    # the applicant has multiple degrees. These scores are independent and
    # only the highest of the two scores is used as the final Degree score
    # reported for the resume.

    # Certification Score:
    # certifications ARE cumulative; each certification on the resume adds
    # its respective score value for the given job role.

    # Grammar Score:
    # spelling and grammar, determined by running the doc through
    # a spellchecker i.e. contextualSpellCheck (spacy universe).
    # Mistakes build up a percentage value that caps at 100%. This
    # value is multiplied by the grammar multiplier and then divided
    # by 100 before being multiplied by the sum of the other scores.

##    "certifications" : { # default values, can be overwritten by the
##                         # certifications field in a given job role
##
##    },

    "junior dev" : {
        "range" : (200,800,),
        "experience" : 100,
        "grammar": 1,
        DEGTYP_IT : { # we want a B.S.
            DEGREE_NULL : 0,
            DEGREE_HS : 25,
            DEGREE_TECHNICAL : 50,
            DEGREE_AA : 50,
            DEGREE_BA : 100,
            DEGREE_BS : 200,
            DEGREE_MASTERS : 400,
            DEGREE_PHD : 600,
        },
        DEGTYP_NONIT : {
            DEGREE_NULL : 0,
            DEGREE_HS : 25,
            DEGREE_TECHNICAL : 50,
            DEGREE_AA : 50,
            DEGREE_BA : 75,
            DEGREE_BS : 150,
            DEGREE_MASTERS : 200,
            DEGREE_PHD : 300,
        },
        "skills" : { # this could replace "experience" field? -- more detailed, same thing
            # (required, +score, *score / year,)
            # required: number of required years of experience
            # +score: score added to experience score simply by the skill being mentioned
            # *score / year: score added to experience score for each year of this skill
            #
            # skills for junior dev are very lenient, just about any IT skill is accepted
            SKILL_JAVA      :(0, 0, 100,),
            SKILL_PYTHON    :(0, 0, 100,),
            SKILL_AWS       :(0, 50, 100,),
            SKILL_JIRA      :(0, 0, 50,),
            SKILL_AGILE     :(0, 0, 100,),
            SKILL_SCRUM     :(0, 0, 100,),
            SKILL_IT        :(0, 0, 100,), # valued less for higher ranked positions
        },
        "certs" : {
            CERT_SUITE_JAVA_FULLSTACK : (NOTREQ, 1,),
            CERT_SUITE_AWS : (NOTREQ, 1,),
        },
    },

    "mid dev" : {
        "range" : (600,1400,),
        "experience" : 100,
        "grammar": 1,
        DEGTYP_IT : { # we want a B.S. or Masters
            DEGREE_NULL : 0,
            DEGREE_HS : 0,
            DEGREE_TECHNICAL : 0,
            DEGREE_AA : 0,
            DEGREE_BA : 300,
            DEGREE_BS : 400,
            DEGREE_MASTERS : 800,
            DEGREE_PHD : 1200,
        },
        DEGTYP_NONIT : {
            DEGREE_NULL : 0,
            DEGREE_HS : 0,
            DEGREE_TECHNICAL : 0,
            DEGREE_AA : 0,
            DEGREE_BA : 150,
            DEGREE_BS : 200,
            DEGREE_MASTERS : 300,
            DEGREE_PHD : 500,
        },
        "skills" : {
        },
        "certs" : {
        },
    },

    "senior dev" : {
        "range" : (1000,2400,),
    },

    "expert dev" : {
        "range" : (2000,99999,),
    },
}

# ~~~ Functions ~~~ #

def get_resume_name(doc) -> str:
    """Get the name of the applicant
    Args:
        doc (spaCy doc): holds the application in a doc object
    Returns:
        str: The name of the applicant
    """
    # return the first PERSON entity in the resume
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent
    # Alternative way: Slower because it proccesses all ents but has advantage of storing every possible name
    # store and return all the PERSON entities in the resume
    # persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    # return persons

def proximity(x, y): # difference of x and y, returns absolute value w/o importing math.
    result = (x - y)
    return result if result >= 0 else -result

        # ~~~ job description weights - getters / setters ~~~ #

def setJD_range_min(jd:str, range_min:int):
    current_max = getJD_range_max(jd)
    POINTS[jd]["range"] = (max(0, range_min), current_max,)
def getJD_range_min(jd:str):
    return POINTS[jd]["range"][0]

def setJD_range_max(jd:str, range_max:int):
    current_min = getJD_range_min(jd)
    POINTS[jd]["range"] = (current_min, max(0, range_max),)
def getJD_range_max(jd:str):
    return POINTS[jd]["range"][1]

def setJD_range(jd:str, range_min:int, range_max:int):
    POINTS[jd]["range"] = (max(0, range_min), max(0, range_max),)
def getJD_range(jd:str):
    return POINTS[jd]["range"]

def setJD_score_experience(jd:str, expmod:int):
    POINTS[jd]["experience"] = max(0, expmod)
def getJD_score_experience(jd:str):
    return POINTS[jd]["experience"]

def setJD_score_grammar(jd:str, grammod:float): # this is a multiplier -- 1 is default
    POINTS[jd]["grammar"] = max(0, grammod)
def getJD_score_grammar(jd:str):
    return POINTS[jd]["grammar"]

def setJD_score_certification(jd:str, certification:str, score:int):
    POINTS[jd]["certifications"][certification] = score
def getJD_score_certification(jd:str, certification:str):
    return POINTS[jd]["certifications"][certification]
def getJD_score_certifications(jd:str):
    return POINTS[jd]["certifications"]

def setJD_score_degree(jd:str, degtype:int, degree:int, score:int):
    POINTS[jd][degtype][degree] = score
def getJD_score_degree(jd:str, degtype:int, degree:int):
    return POINTS[jd][degtype][degree]

def getJD_list():
    return [*POINTS]

# ~~~ Classes ~~~ #



''' container for information about a degree
    with some helpful functions
'''
class Degree:
    def __init__(self, name:str, major:str, score):
        self.name=name
        self.major=major
        self.score=score
    def __str__(self):
        return DEGREES[self.name] + " in " + self.major
    @classmethod
    def typeOf(cls, major:str): # returns DEGTYP_ const int
        return FIELDS.get(major, DEGTYP_NONIT)
    def getType(self, major=None): # returns DEGTYP_ const int
        if not major:
            major=self.major
        return Degree.typeOf(major)

''' Object to Analyze Resumes as string or spacy Doc
    Usage:
        make sure the desired model (small, medium, or large) is installed on your machine.
        instantiate class with the desired model as a parameter e.g.
            analyzer = ResumeAnalyzer("large")
        Then, use one of the analyze functions to analyze your resumes.
        analyzeFile takes a complete file directory as a string.
            analyzer.analyzeFile("junior dev", "C:/Users/Me/Desktop/myfile.pdf")

'''
class ResumeAnalyzer:
    WEIGHT_EXPERIENCE   = 100   # can be up to double this value
    WEIGHT_CERTS        = 1.0
    WEIGHT_GRAMMAR      = 100   # and/or spelling
    WEIGHT_DICTION      = 50
    WEIGHT_STARRED      = 150
    WEIGHT_REJECTED     = -150

    def __init__(self, model="small", role=None):
        '''
            spaCy v3.0 models:
                small:  en_core_web_sm  | 13 MB
                medium: en_core_web_md  | 44 MB
                large:  en_core_web_lg  | 742 MB
        '''
        if model=="small":
            modelID = "en_core_web_sm"
        elif model=="medium":
            modelID = "en_core_web_md"
        elif model=="large":
            modelID = "en_core_web_lg"
        else:
            modelID = None

        if modelID:
            self.nlp = spacy.load(modelID)
        else:
            raise Exception('''ResumeAnalyzer: cannot instantiate.
Reason: invalid parameter 'model'.
Expected: 'small', 'medium', 'large' | Given: {}'''.format(model))

        self.role = role    # selected job description
        self.last = {}
    # end def

    def setRole(self, role:str):
        self.role = role
    def getRole(self):
        return self.role

    def analyzeFile(self, directory: str, role=None):
        #TODO!
        pass

    def analyzeText(self, resumeText: str, role=None):
        Test.test("type(resume) is str: ", statement=type(resumeText) is str)
        self.analyze(self.nlp(resumeText), role=role)

    def analyze(self, resume: spacy.tokens.doc.Doc, role=None) -> int:
        '''
            Analyze the given resume across the given job role, and return
                an integer 0-100 representing how well it matches the role.
        '''

        '''TODO:
            take in params from user
                job description
            user can set certifications / weights for a job description
            take in pdf file, spit out resume analysis.

        NICE TO HAVE / ULTIMATELY:
            save resume analysis as its own file (?) / stash / database it
            load from resume analysis file
'''

        Test.test("type(resume) is spacy.tokens.doc.Doc: ",
             statement=type(resume) is spacy.tokens.doc.Doc )
        Test.test("type(role) is str or NoneType: ",
                  statement=type(role) is str or type(role) is type(None))

        if role==None:
            if self.role==None:
                print("Failed to analyze resume!")
                print("Call setRole(role:str) before analyzeText(...).")
                return 0
            role = self.role

        final_score = 0
        score_exp = 0
        score_degree = 0
        score_grammar = 0
        score_diction = 0
        degrees = []
        degree = Degree(DEGTYP_NULL, "N/A", 0)

        applicantName = get_resume_name(resume)

        # degrees
        matches = self._getDegreeMatches(resume)
        for match_id, start, end in matches:
            match_class = self.nlp.vocab.strings[match_id]

            searchdist = 12 # don't search too far
            closest = 9999
            this_major = None # name of the major in human-legible English
            fmatches = self._getFieldMatches(resume, start - searchdist, end + searchdist)
            for fmatch_id, fstart, fend in fmatches:
                prox = proximity(fstart, start)
                if prox < closest:
                    closest = prox
                    this_major = self.nlp.vocab.strings[fmatch_id]

            if this_major:
                major_type = Degree.typeOf(this_major)
                this_score = POINTS[role][major_type][match_class]
                degreeObj = Degree(match_class, this_major, this_score)
                degrees.append(degreeObj)

                Test.test("Degree: Match found: {}, major {} (class: {} | type: {})".format(
                    resume[start:end].text, this_major, match_class, degreeObj.getType()))

        # end for
        # pick ONLY the degree with the highest score
        for deg in degrees:
            if deg.score > score_degree:
                degree = deg
                score_degree = deg.score
        if degree: # add the degree score
            score_exp += score_degree

        # skills
        # get dict of skills {skill : experience}
        #   where experience is an int or quality adjective
        skillmatcher = SkillMatcher(resume)
        skillset = skillmatcher.getExperience()
        # parse into {skill : yearScore} where yearScore is an int
        skillexp, skills = self._parseSkillData(skillset)
        expmod = POINTS[role]["experience"]
        score_exp += skillexp*expmod # add the experience score
        toRemove = []
        for k in skills.keys():
            if skills[k] <= 0:
                toRemove.append(k)
        for k in toRemove:
            del skills[k]

        # certifications (TEST!)
        score_certs = 0
        certlis = []
        certdict = {}
        for certid,data in POINTS[role]["certs"].items():
            req,cert = data
##            certlis.append(CERTIFICATIONS[certid])
##            certdict.update({cert:req})
        certmatcher = CertMatcher(role, resume, certlis)
        certset = certmatcher.getMatches()
        for cert in certset:
            if certdict[cert] == REQUIRED:
                score_certs = -100
                break
            score_certs += CERTIFICATIONS[cert][1]
        #

        exprng = POINTS[role]['range']
        isMatch = self._isMatch(exprng, score_exp)
        self._reportResumeData(
            applicantName, role, isMatch, degree, skills, score_exp, exprng
            )

        final_score = self._calcFinalScore(
            score_exp, exprng, score_certs, score_grammar, score_diction,
            False, False
            )

        return final_score
    # end def


    def getLastName(self):
        return self.last["name"]
    def getLastJD(self):
        return self.last["job"]
    def getLastMatch(self):
        return self.last["is_match"]
    def getLastDegree(self):
        return self.last["degree"]
    def getLastSkills(self):
        return self.last["skills"]
    def getLastExpScore(self):
        return self.last["exp_score"]
    def getLastExpRange(self):
        return self.last["exp_range"]

    def sortedSkills(self):
        skillset = self.last['skills']
        return sorted(skillset, key=skillset.get, reverse=True)

    def _checkGrammar(self, resume:spacy.tokens.doc.Doc):
        pass

    def _calcFinalScore(self,
        score_exp:int, exprng:tuple, score_certs:int,
        score_grammar:float, score_diction:float,
        starred:bool, rejected:bool
        ):
        final_score = 0

        mid_exp = (exprng[0] + exprng[1]) / 2
        exp_a = proximity(exprng[1], mid_exp)
        prox = proximity(score_exp, mid_exp)
        # X if you're in range, + 0-X for how close to center of range.
        final_score += (prox <= exp_a)*self.WEIGHT_EXPERIENCE
        final_score += max(0, self.WEIGHT_EXPERIENCE - round(
            prox / exp_a * self.WEIGHT_EXPERIENCE
            ))

        final_score += round(score_certs*self.WEIGHT_CERTS)
        final_score += round(score_grammar*self.WEIGHT_GRAMMAR)
        final_score += round(score_diction*self.WEIGHT_DICTION)
        final_score += starred*self.WEIGHT_STARRED
        final_score += rejected*self.WEIGHT_REJECTED
    # end def

    def _isMatch(self, rng, score_exp):
        return "Yes" if (rng[0] <= score_exp and rng[1] >= score_exp) else "No"

    def _getDegreeMatches(self, resume: spacy.tokens.doc.Doc) -> list:
        matcher = spacy.matcher.Matcher(self.nlp.vocab)

        # -- add in the patterns -- #

        # degrees
        # A.A.
        matcher.add(DEGREE_AA, PATTERNS[DEGREE_AA])
        # B.A.
        matcher.add(DEGREE_BA, PATTERNS[DEGREE_BA])
        # B.S.
        matcher.add(DEGREE_BS, PATTERNS[DEGREE_BS])
        # Masters
        matcher.add(DEGREE_MASTERS, PATTERNS[DEGREE_MASTERS])
        # Ph.D.
        matcher.add(DEGREE_PHD, PATTERNS[DEGREE_PHD])

        # run the match on the patterns
        return matcher(resume)
    # end def

    def _getFieldMatches(self, resume:spacy.tokens.doc.Doc, start, end) -> list:
        matcher = spacy.matcher.Matcher(self.nlp.vocab)

        # -- add in the patterns -- #

        for field,clas in FIELDS.items():
            pattern = []
            for s in field.split(' '):
                pattern.append({"LOWER": s.lower()})
            matcher.add(field, [pattern])

        # run the match on the patterns
##        print(resume[start : end])
        return matcher(resume[start : end])
    # end def

    def _reportResumeData(self,
        name:str, job:str, is_match:bool, degree:Degree, skillset:dict,
        exp_score:int, rng:tuple
        ):
        ''' Once all the data is collected, output it to the user
            name: applicant name, string
            job: role, string
            isMatch: does the applicant match the job description? bool
            degree: Degree object -- the highest scoring degree in the resume
            skillset: dict in the format {skill : score OR quality-string}
            score: # years experience in related skills, total (non-cumulative), int
            rng: range of experience score for the given JD
        '''

        # remember the data of this applicant
        self.last["name"] = name
        self.last["job"] = job
        self.last["is_match"] = is_match
        self.last["degree"] = degree
        self.last["skills"] = skillset
        self.last["exp_score"] = exp_score
        self.last["exp_range"] = rng

        print("~~~~~~~~~~~~~~~~~~")

        print("Applicant Name:        {}".format(name))
        print("Applying for position: {}".format(job))
        print("Education:             {} / {} (+{})".format(DEGREES[degree.name], degree.major, degree.score//100))
        print("Standardized Score:    {} (years experience)".format(exp_score//100))
        print("Score range:           {} - {}".format(rng[0]//100, rng[1]//100))
        print("Match for role?        {}".format(is_match))

        print("--- Skills ---\nSkill Name\t\t\t\tYears Experience")
        for k in sorted(skillset, key=skillset.get, reverse=True):
            print("\t{k}:".format(k=k).ljust(36, '.'),end="")
            print(skillset[k])

        print("End of report.\n")
    # end def

    def _parseSkillData(self, skillset:dict) -> tuple:
        ''' input: dict of skills where values may be string quality adjectives or ints,
            output: dict of skills where values are all integers
        '''
        totalExp = 0
        qualitySkills = {}
        returnSkills = {}

        for k,v in skillset.items():
            intValue = self._parseInt(v)
            if intValue is not None:
                skillExp = intValue
                totalExp = max(skillExp, totalExp)
                returnSkills.update({k:v})
            else:
                qualitySkills.update({k:v})

        for k,v in qualitySkills.items():
            skillExp = self._parseQualityLevel(totalExp, v)
            returnSkills.update({k:skillExp})

        return (totalExp, returnSkills,)
    # end def

    def _parseInt(self, string: str):
        try:
            i = float(string) # parse as a float first so we catch decimals
            return int(i)
        except:
            return None

    def _parseQualityLevel(self, totalExp:int, string:str):
        multiplier = totalExp if totalExp > 0 else MINIMUM_EXP
        return math.ceil(multiplier * QUALITIES.get(string, 0))

# end class


# Terminal Interface

def printState(resumeAnalyzer : ResumeAnalyzer):
    print("Job description: ", resumeAnalyzer.getRole())

def printMenu(resumeAnalyzer : ResumeAnalyzer):
    print('''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Job Description: {}
Command......Action
R............analyze Resume file (.pdf)
J............set selected Job description
W............set Weights for selected job description
'''.format(resumeAnalyzer.role))

if __name__=="__main__":
##    Test.enableAssertions()
    Test.enableDebugMode()

    resumeString = ''' https://eyecube.github.io
eyecube1@protonmail.com
850-524-9998
2731 Blair Stone Rd Tallahassee FL, 32301
Jane Wharton
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

    # TODO: add education experience to Standardized Score

##    print("JD list: ", getJD_list())

    ra = ResumeAnalyzer()

##    while True:
##        printMenu(ra)
##        inp = input("Enter a command: ")


    ra.setRole("junior dev")

    ra.analyzeText(resumeString)

##    resan.analyzeText("junior dev", resumeString)
    print("Done.")
