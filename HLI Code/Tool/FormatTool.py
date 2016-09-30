class FormatTool():

    @classmethod
    def norm_str(cls, str):
        if(str == None or str == ""):
            str="0"
        return str
        
    @classmethod
    def float_str_to_float(cls, str):
        str = FormatTool.norm_str(str)
        f = float(str)
        return f


    @classmethod
    def floatStrToInt(cls, str):
        #n = 0
        if(str == ""):
            str = "0"

        n = int(round(float(str)))
        #try:
        #    n = int(round(float(str)))
            #print "str: %s" % str
            #print "n: %d" % n
        #except:
        #    print "str is not digit: $%s$" % str

        return n

    @classmethod
    def intStrToInt(cls, str):
        if(str == ""):
            str="0"

        n=int(str)
        return n