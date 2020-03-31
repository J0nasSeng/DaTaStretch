from datastretch.core import Task

import os

class ProcessingTask1(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        self.data = "This data will be passed to my successor."
        return self.data


class ProcessingTask2(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        self.data = "This data will be passed to my successor."
        return self.data
