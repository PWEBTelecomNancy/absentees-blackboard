__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from model.ADECommunicator import *
from handler.BaseHandler import *

class FlushHandler(BaseHandler):
    ade = ADECommunicator()

    def get(self):
        self.ade.preload()
        self.write("Refreshed lessons.")
