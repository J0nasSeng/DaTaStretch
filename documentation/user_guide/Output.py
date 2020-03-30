from core.Task import Task


class Output(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I will calculate the output!")
