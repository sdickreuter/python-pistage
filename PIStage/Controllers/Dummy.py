__author__ = 'sei'

from PIStage._base import Controller
import time

class Dummy(Controller):

    def __init__(self, port=None):
        print('Dummy initialized')

    def pos(self):
        time.sleep(0.05)
        return 10,10,10

    def moveabs(self, x=None, y=None, z=None):
        time.sleep(0.05)

    def moverel(self, dx=None, dy=None, dz=None):
        time.sleep(0.05)

    def home(self):
        time.sleep(0.05)
