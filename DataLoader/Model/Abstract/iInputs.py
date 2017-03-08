
from Model import *

class iInputs():

    def parse(self):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()

    def sendODM2Session(self):
        raise NotImplementedError()
