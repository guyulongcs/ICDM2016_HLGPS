class Evaluation():
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0

    def SetValue(self, tp, fp, tn, fn):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn

    def evaluate(self):
        self.precision = self.tp / (float(self.tp + self.fp))
        self.recall = (self.tp ) / (float(self.tp + self.fn))
        try:
            self.f1 = 2 * self.precision * self.recall / (self.precision + self.recall)
        except:
            pass

        print "precision:%.3f, recall: %.3f, f1:%.3f" % (self.precision, self.recall, self.f1)

