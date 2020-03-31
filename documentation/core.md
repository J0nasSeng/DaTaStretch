## core
The core-module provides the basic classes the framework is made of. This includes Tasks and the Registry.

### Task
Task objects are the basic unit of each pipeline. A Task can be considered as a node in a directed graph (DAG).
Tasks are connected with one or more other tasks by edges which represent the data-flow.

As the name suggests, tasks are not static, they contain actions to be executed. These actions are defined by the
developer implementing the `run()`-method. To do so, you have to create a child-class of `Task` and inherit from it.
By implementing `run()` you can specify the actions done when the task is started in the pipeline.

IMPORTANT: Never overwrite any other method of Task, this will lead to errors, often the its dependencies then
            no longer can be found.

### Methods
`run(self, *args, **kwargs)`: Method to be implemented by a child-class of `Task`.

`run_args(self, *args, **kwargs)`: Set the arguments that should be passed to `run()`.

`dependency(self, *obj: Task)`: By calling this method on a `Task`-object the dependencies of this task can be set by
passing other `Task`-objects.

`get_dependency(self)`: Returns an iterator used to iterate over all dependencies of a `Task`-object.

`get_dependencies(self)`: Returns all dependencies of a `Task`-object as a list.

`move_data(self, successors: List['Task'], result: any) -> None`: Called by the pipeline to
move the data from one task to all its successors. How the access in the successors can be
made, is shown in `attr_access_as`.

`attr_access_as(self, access: str) -> None`: With this method you can specify how you want to
access the data of the ancestors of your task. If 'attr' is your choice, you can easily 
access data via a variable reference. This means your task contains a variable whose name
is the name of the task the data was sent from, lowered. Example: If your task receives
data from a task named 'Loader', then you can access its data via 'self.loader_data'. If
you choose 'dict' as the access-type, you can access the data of 'Loader' via a dictionary-
lookup where self.data is the dictionary and 'loader_data' is the key.

`receive(self, data: any, sender: str) -> None`: This method is called when data is moved
from one task to its successors. The caller-method of ``receive`` is `move_data`. You are free
to overwrite `receive`, but be careful with this, it can lead to errors hard to debug.