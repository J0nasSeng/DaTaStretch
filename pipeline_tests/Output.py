from datastretch.core import Task

import os

class Output(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("Output: I received from ProcessingTask2:")
        print(self.processingtask2_data)
