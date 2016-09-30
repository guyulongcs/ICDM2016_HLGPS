from FileTool import *
class Test():
    i=1;
    @classmethod
    def start(cls):
        test=Test()
        test.add()


    def __init__(self):
        pass;

    def add(self):
        Test.i=Test.i+1
        print Test.i;

if __name__=="__main__":
    Test.start()