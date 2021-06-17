'''
Author: Jane Wharton
Company: Geek Sources, Inc.

test.py: debug and assertions

'''

class Test:
    ASSERTMODE = False
    DEBUGMODE = False
    
    @classmethod
    def test(cls, text: str, statement=None):
        if statement is not None:
            if cls.ASSERTMODE:
                if cls.DEBUGMODE:
                    print(text, end="")
                assert(statement)
                if cls.DEBUGMODE:
                    print("Passed.")
        elif cls.DEBUGMODE:
            print(text)
    @classmethod
    def getDebugMode(cls):
        return cls.DEBUGMODE
    @classmethod
    def getAssertMode(cls):
        return cls.ASSERTMODE
    @classmethod
    def enableDebugMode(cls):
        cls.DEBUGMODE = True
    @classmethod
    def disableDebugMode(cls):
        cls.DEBUGMODE = False
    @classmethod
    def enableAssertions(cls):
        cls.ASSERTMODE = True
    @classmethod
    def disableAssertions(cls):
        cls.ASSERTMODE = False
