from core.Task import Task


class LoaderSource1(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am Loader number 1!")
        self._flow_data = "This data will be passed to my successor."


class LoaderSource2(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am Loader number 2!")
        self._flow_data = "This data will be passed to my successor."


class LoaderSource3(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self, example_arg):
        print("I am Loader number 3 and get argument {}".format(example_arg))
        self._flow_data = "This data will be passed to my successor."
