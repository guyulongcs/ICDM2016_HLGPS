import sys


class InOut():
    @classmethod
    def console_func_begin(cls, str):
        print "\n%s begin..." % str

    @classmethod
    def console_func_end(cls, str):
         print "\n%s end..." % str

    @classmethod
    def except_info(cls, str):
        print "\nExcept in %s!" % str

        print "Unexpected error:", sys.exc_info()[0]

    @classmethod
    def debug(cls, str, debugMode=True):
        if(debugMode):
            print "debug...\t%s" % str
