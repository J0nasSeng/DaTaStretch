from core.Task import Task


class ProcessingTask1(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am processing class 1!")
        self._flow_data = "This data will be passed to my successor."


class ProcessingTask2(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am processing class 2!")
        self._flow_data = "This data will be passed to my successor."
