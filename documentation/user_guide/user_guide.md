# User Guide
This document is a guide how to use DaTaStretch. 

## Installation
First install DaTaStretch if you haven't done yet. To do this, just type
``pip install datastretch`` into your console.

## Import
After installation you are able to import the packages provided. 
The most important ones are ``core`` and ``pipeline``. These two will
be the only modules you will deal with in this guide and are enough to
build a fully parallelized pipeline. To import type:
````python
from datastretch.pipeline import Pipeline
from datastretch.pipeline import Stage
from datastretch.core import Task
````

## Defining Tasks
Next you have to define a few tasks that should be executed by the pipeline.
Therefore you have to create a few classes inheriting from ``Task``.
Each of this classes has to implement the ``run()``-method. 

### Loader-classes
Let's design an example in which we want to download data from three
different sources. As a next step we want to process the downloaded data
and as a last step a result should be calculated on the processed data.
This is a very common pattern in data science-scenarios for example.

In the following example-code the classes won't download any data, they
are just representatives of such classes. The same holds for the processing
classes, each of them will only print their name to console and exit. 
Furthermore they will set the member-variable ``self._flow_data``. For now
just ignore this line, later we will see why this is set. 
Let's see how these classes look like:
````python
class LoaderSource1(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am Loader number 1!")
        self._flow_data = "This data will be passed to my successor."
````
````python
class LoaderSource2(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am Loader number 2!")
        self._flow_data = "This data will be passed to my successor."
````
````python
class LoaderSource3(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self, example_arg):
        print("I am Loader number 3 and get argument {}".format(example_arg))
        self._flow_data = "This data will be passed to my successor."
````
As you can see, the ``run()``-method of the third class gets
and argument. This is absolutely legal, later on we will tell the pipeline
which arguments it has to pass to this method. You are free to pass any 
number of arguments to your ``run()``-method to guarantee a maximum of 
freedom in implementing your tasks.

### Processing classes
In this and the next section only the definitions of the classes are shown
without any further explanation, it follows straight the definitions of the
Loader-classes.
````python
class ProcessingTask1(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am processing class 1!")
        self._flow_data = "This data will be passed to my successor."
````
````python
class ProcessingTask2(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I am processing class 2!")
        self._flow_data = "This data will be passed to my successor."
````

### Output-class
````python
class Output(Task):
    
    def __init__(self):
        # do your init-stuff here
        super().__init__()

    def run(self):
        print("I will calculate the output!")
````

## Defining Dependencies
There is one more information the pipeline needs to be able to execute 
our tasks safely. We have to define dependencies among the tasks. For this
purpose we can use the ``dependency()``-method of the `Task`-class or
we can define them while defining stages which is described below. Due to
the better readability in this guide only the way of defining them via the
``dependecy()``-method is shown.

To define dependencies instantiate your defined tasks:
````python
loader1 = LoaderSource1()
loader2 = LoaderSource2()
loader3 = LoaderSource3()

pt1 = ProcessingTask1()
pt2 = ProcessingTask2()

out = Output()
````
Now let's define the dependencies among them:

````python
# pt1 has to wait for loader1:
pt1.dependency(loader1)

# pt2 has to wait for loader2 and loader3
pt2.dependency(loader2, loader3)

# output has to wait for both processing-objects
out.dependency(pt1, pt2)
````
There is one thing left we have to do. As you remember the definition of the
LoaderSource3-class, the run-method of this class takes an argument. We now will
tell the pipeline which arguments it has to pass to this task by calling the following:
````python
loader3.run_args('Our argument')
````
This will make the pipeline recognizing that this loader needs an argument to run. 
This method works for a arbitrary number of positional arguments, you can also pass 
optional arguments. Then you have to specify the arguments name and then its value as you
are familiar with from Python:
````python
loader3.run_args(optional_arguemnt='Optional argument')
````
You can also combine this:
````python
loader3.run_args('Our argument', optional_arguemnt='Optional argument')
````
But we don't want to pass any optional arguments, so we are fine with the first call of
``run_args()``.

Now all dependencies are defined and we can proceed with defining the pipeline.

## Defining Stages
Now all tasks are defined and we are ready to clip them together step by step.
For this purpose the easiest (but not the only way) is to define stages
which are then used to build up our pipeline. As the last sentence implies
there is another way to do this, but this way is not shown here.

We need three stages: One for the loaders, one for the processing-objects and
one for the output:
````python
stage1, stage2, stage3 = Stage(), Stage(), Stage()

stage1.add(loader1)
stage1.add(loader2)
stage1.add(loader3)

stage2.add(pt1)
stage2.add(pt2)

stage3.add(out)
````

## Defining the Pipeline
Now we are ready to do the last step: Defining the pipeline.
To do this, create a ``Pipeline``-object, add the stages, compile the
pipeline and you can run it. The ``pipeline.compile()``-call will
make the pipeline creating an _execution graph_ which defines in which
order the tasks will be executed and which can be run in parallel.
You can plot this graph with the call ``pipeline.plot('execution')``, with
``pipeline.plot('task')`` you can plot a graph of your defined pipeline.
````python
pipeline = Pipeline()
pipeline.add(stage1)
pipeline.add(stage2)
pipeline.add(stage3)

pipeline.compile()
# you can plot those if you want to:
# pipeline.plot('task')
# pipeline.plot('execution')
if __name__ == '__main__':
    pipeline.run()
````
It is important to run the pipeline within the 
``if __name__ == '__main__':'``-block, otherwise you
will get multiprocessing-errors.
Now you are ready to build your own pipelines, have fun!
