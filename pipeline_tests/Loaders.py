from datastretch.core import Task

class LoaderSource1(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        self.data = "This data will be passed to my successor."
        return self.data


class LoaderSource2(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        self.data = "This data will be passed to my successor."
        return self.data


class LoaderSource3(Task):

    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self, example_arg):
        self.data = "This data will not be passed to my successor."
