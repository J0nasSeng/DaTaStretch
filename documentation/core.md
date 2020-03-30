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