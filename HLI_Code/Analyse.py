__author__ = 'guyulong'

from Tool import InOut
from Tool.InOut import *
from AnalyseVenue import *
from AnalyseUser import *
from AnalyseCheckin import *
from AnalyseFriend import *

class Analyse():
    def __init__(self):

        pass

    def start(self):
        InOut.console_func_begin("Analyse start")

        analyseVenue = AnalyseVenue()
        #analyseVenue.start()

        analyseUser = AnalyseUser()
        #analyseUser.start()

        analyseCheckin = AnalyseCheckin()
        #analyseCheckin.start()

        analyseFriend = AnalyseFriend()
        analyseFriend.start()