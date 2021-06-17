'''
Author: Jane Wharton
Company: Geek Sources, Inc.

diction.py:

    This module is designed to analyze the diction of a text and return
        a value representing its "uniqueness" or how common the words it
        contains are when compared against the databases stored in the
        wordfreq library.

    Example use of TriteWords.test for assertions / debug:
        debug print statement example
            cls.test("found word: {}!".format(word))
        assertion example
            cls.test("type(word) is str: ",
                 statement=(type(word) is str), assertion=True
                 )

    
'''
import spacy # pip install spacy
import contextualSpellCheck # spacy
#import json
import wordfreq # pip install wordfreq

from jtest import Test

class TriteWords:

    cutoff_rare     = 2
    cutoff_uncommon = 4
    cutoff_trite    = 5

    weight_unique   = 50
    weight_rare     = 10
    weight_uncommon = 1
    weight_trite    = -5
    weight_common   = 0
    
##    _NUMSETS = 3
##    _words=[set() for _ in range(_NUMSETS)]


    @classmethod
    def setCutoffRare(cls, value): cls.cutoff_rare = value
    @classmethod
    def setCutoffUncommon(cls, value): cls.cutoff_uncommon = value
    @classmethod
    def setCutoffTrite(cls, value): cls.cutoff_trite = value
        
    @classmethod
    def getFreq(cls, word:str):
        Test.test("type(word) is str: ", statement=(type(word) is str))
        return cls._getFreq(word)
    @classmethod
    def _getFreq(cls, word:str):
        return wordfreq.zipf_frequency(word, "en")

    @classmethod
    def analyze(cls, wordList: list):
        ''' size of cutoffs should be 1 less than _NUMSETS at maximum,
            because the last cutoff is just anything left over. '''
        
        cnt_unique = 0
        cnt_rare = 0
        cnt_uncommon = 0
        cnt_trite = 0
        cnt_common = 0
        
        for word in wordList:
            Test.test("type(word) is str: ",
                 statement=(type(word) is str)
                 )

##            ''' find word in our sets if possible, before using wordfreq '''
##            for i in range(cls._NUMSETS):
##                if word in cls.words[i]:
##                    Test.test("found word index {}: {}!".format(i, word))
##                    cnt[i] += 1
##                    break
##
##            else:
##            index = cls._NUMSETS - 1
            freq = cls._getFreq(word)
            if freq==0:
                cnt_unique += 1
            elif freq<=cls.cutoff_rare:
                cnt_rare += 1
            elif freq<=cls.cutoff_uncommon:
                cnt_uncommon += 1
            elif freq<=cls.cutoff_trite:
                cnt_trite += 1
            else:
                cnt_common += 1
                    
##                for i in range(len(cutoffs)):
##                    if (freq > 0 and freq <= cutoffs[i]):
##                        index = i
##                        break
##                cls.words[index].add(word)
        return (cnt_unique, cnt_rare, cnt_uncommon, cnt_trite, cnt_common,)

    @classmethod
    def printAnalysis(cls, wordList: list):
        uni,rar,unc,tri,com = cls.analyze(wordList)
        print("unique words: ", uni)
        print("rare words: ", rar)
        print("uncommon words: ", unc)
        print("trite words: ", tri)
        print("common words: ", com)
# end class
        
if __name__=="__main__":
    #print("a" in {"w":1})
    TriteWords.enableDebugMode()
    TriteWords.enableAssertions()
    
    TriteWords.printAnalysis([
        "developer", "develop", "developed", "developing",
        "team"
        ])
    TriteWords.printAnalysis([
        "worked", "work", "working", "do", "doing"
        ])
    TriteWords.printAnalysis([
        "dandy", "dandelion", "dander", "dan",
        ])
# end if



        



