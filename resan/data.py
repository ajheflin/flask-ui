'''
Company: Geek Sources, Inc.

data.py: database / applicant / resume data storage

'''

from jtest import Test

class Resume:
    def __init__(self):
        pass

class Applicant:
    MAX_RATING = 5
    STARRED_SCORE = 100
    REJECTED_SCORE = -100

    def __init__(self, name:str, rating=0, resumes=[]):
        self.name = name
        self.rating = rating    # overall rating
        self.resumes = []
        self.addResumes(resumes)
        self.starred = 0    # 0 or 1
        self.rejected = 0   # "
        self.seen = 0       # "

    def setRating(self, rating:int): # overall rating
        Test.test("type(rating) is int", statement=type(rating) is int)
        self.rating = max(0, min(rating, cls.MAX_RATING))
    def getRating(self): # calculate overall rating
        return self.rating + self.starred*STARRED_SCORE + self.rejected*REJECTED_SCORE
    
    def setSeen(self, value=1):
        Test.test("value int == 0 or 1", statement=(value <= 1 and value >= 0))
        self.seen = value
    def see(self):
        self.setSeen(1)
    def unsee(self):
        self.setSeen(0)
    def getSeen(self):
        return self.seen

    def addResume(self, resume:Resume):
        Test.test("addResume: type(resume) is Resume",
                  statement=type(resume) is Resume)
        self.resumes.append(resume)
    def addResumes(self, resumes:list):
        for resume in resumes:
            Test.test("addResumes: type(resume) is Resume",
                      statement=type(resume) is Resume)
            self.addResume(resume)

##
##class Database:
##    def __init__(self):
##        self.applicants=[]
##    def addApplicant(self, applicant:Applicant):
##        Test.test("type(applicant) is Applicant",
##                  statement=type(applicant) is Applicant)
##        self.applicants.append(applicant)
##    def getApplicant(self, query:str):
##        pass
