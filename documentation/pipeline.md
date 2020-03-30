## pipeline
The pipeline-module is the module you probably will interact most of the time. This module contains the
`Pipeline`-class and the `Stage`-class. Both are the basic classes when building a pipeline.

#### Variables
pipeline provides one global variable `MAX_PIPELINES` which defines how many pipelines can be created.
It is set to *1000* by default and may be changed to restrict the resource consumption.

### Pipeline
Pipelines are directed acyclic graphs defining a data-flow. You are responsible for defining the data-flow
and what has to be done in the certain steps of the pipeline. The rest is done by the `Pipeline`-object.
This includes scheduling of tasks, starting tasks, collecting and sending data among tasks and so on.

The `Pipeline`-class provides easy access to the pipeline and builds the acyclic directed graph (from now on
referred to as _task graph_) automatically when you call the `add()`-method. Furthermore when calling the
`run()` method another directed acyclic graph - the _execution graph_ gets built. This graph defines the
order the tasks get scheduled and executed. Due to the parallel processing of the pipeline-framework
another task which is done by the `Pipeline` is the mapping between tasks and processes. You can define
how many processes should be used. Note that processes are created to implement parallelism because
Python-threads do not support real parallel processing.

CAUTION: Launching too many processes can lead to bad performance when processing. The standard number of
processes is set to the double of available CPU-cores of your machine.

#### Methods
`run(self) -> None`: Freezes the task-graph, generates an execution-graph if it was not done yet
and executes the defined tasks based on the execution-graph.

`add(self, task_or_stage: Task or Stage) -> Pipeline`: Adds a `Stage` or a task to the pipeline. When adding a stage, all
dependencies of the tasks must be set. When adding a `Task` the dependency will be automatically be resolved
if it is set in the passed object. If not, the object gets placed in the last stage independently.

`compile(self)`: When this method is called, the execution graph will be built. You do not have to call it
before calling `run()`, this will be implicitly be done if `compile()` wasn't called yet. Especially for
debugging-purposes it is a good practice to call `compile()` and then `plot()` to check whether the
pipeline and the execution graph look as you expected.
The method checks whether cycles exist in the task graph. If it is the case, a CompilationError will be raised.

`plot(self, graph: str # 'task') -> None`: If the `graph`-argument is equal to 'task', the task graph will be
plotted, if it is equal to 'execution', the execution graph will be plotted.

`_add_stage(self, stage: stg.Stage) -> None`: Private method for adding a stage.

`_add_task(self, task: co.Task) -> None`: Private method for adding a task.

`_exec_execution_graph(self) -> None`: Private method to execute the _execution graph_ using breadth
first search (bfs). This guarantees that the tasks are executed in the correct order with respect to
their dependencies. Furthermore the master-process blocks the execution of tasks being dependent on
tasks that are still in execution or are not executed yet.

`_exec_nodes(self, tasks: Iterable) -> None`: Private method acting as a helper-method for the bfs while
task-execution. It executes one level of the execution graph and waits until it is finished.

`_create_batches(self, tasks: List[co.Task]) -> List[List[co.Task]]`: In case that not enough resources
(processors) are available such that all parallelizable tasks can be run in parallel, they will be split into
batches. These batches will be executed sequentially.

`_check_cycles_freedom(self) -> bool`: Private method which tries to find cycles in the task graph.
If no is found, True is returned, else False is returned.

IMPORTANT: Before calling `plot(graph#'execution')` you have to call `compile()`

`_add_stage(self, stage: stg.Stage) -> None`: Private method used to add a new `Stage` in the pipeline.

`_add_task(self, task: co.Task) -> None`: Private method used to add a new `Task` in the pipeline.

`_exec_execution_graph(self) -> None`: A private method to execute the generated _execution graph_.

`_next_tasks(self, result, tsk: co.Task) -> None`: Called by `_exec_execution_graph()` to get the next ready
tasks to be executed. It dynamically updates the _execution graph_ as long there are tasks to be run.

#### Variables
`MAX_PROCESSES`: Define the maximum number of processes to be launched by the pipeline.

`task_graph`: Stores a `nx.DiGraph`-object in it which represents the task graph.

`stages`: List of lists, stores the stages of the pipeline and so represents the hierarchy.

`scheduler`: Object of the `Scheduler`-class, used to generate the _execution graph_.

`execution_graph`: Stores the execution graph which is used to determine the order tasks are launched.

`_hash`: Private variable, containing a random integer which is returned by the __hash__-method.

`_start_nodes`: Private variable holding a list of tasks to be started in next round.

`_process_pool`: Private. A `Pool`-object of the `multiprocessing`-module of Python.

`_last_task`: Private. The last task to be executed in the pipeline, used to check if pipeline is done.

CAUTION: Launching too many processes can lead to bad performance when processing. The standard number of
processes is set to the double of available CPU-cores of your machine.

### Scheduler
The `Scheduler`-class is responsible for generating the _execution graph_. You should not have to interact
with this class at all but if you do this won't cause problems.

#### Methods
`generate_execution_graph(self, task_graph: nx.DiGraph, stages: List['stg.Stage']) -> (nx.DiGraph, List[task.Task])`:
This method generates the _execution graph_ which is used to schedule your tasks. It returns a
`networkx.DiGraph`-object as well as a list of the first nodes to be run. If you call this method from outside,
it will not have an impact on the associated pipeline-object.

`_find_ready(self, stage: stg.Stage, last_run: List[Task]) -> List[Task]`: Private helper-method that finds
ready tasks (i.e. tasks without dependencies) in a given stage.

`_remove_dependencies(self, tsk: task.Task) -> None:`: Helper-method to remove all dependencies of a given
tasks. The generation of the _execution graph_ is an iterative process. In each round for each stage one task
is specified that has no dependencies anymore and so can be safely executed if there is such a task.
To avoid stucking in this iterative process it is required to remove the found dependency-free task from all
dependency-lists of other tasks it is stored in.

#### Variables
`execution_graph`: _execution graph_ is stored here if finished creating it.

`task_graph`: _task graph_ given by the caller of `generate_execution_graph`

`nodes`: All tasks stored as a list.

`task_to_dependencies`: Dictionary storing all dependencies for a given task. The task is the key.


### Stage
Beside tasks stages are another basic module of pipelines. You can think about stages
as containers for tasks. They aggregate tasks sharing the same stage in the pipeline, this
means the tasks inside a stage are independent from each other.

#### Methods
`add(self, tsk: task.Task, dependency: task.Task # None) -> 'Stage')`: Use this
method to add a task to a stage. It takes two `Task`-objects as input, the first one
is the object to be added to the stage, the other one is a dependency to a task of another
stage. The dependency-argument is optional. If you set the dependencies when creating
tasks, you do not have to pass it.
The method returns the new `Stage`-object

`remove(self, tsk: task.Task) -> 'Stage'`: Use this method to remove a task from
a stage.

`tasks(self)`: Returns an iterator over all tasks of the `Stage`-object.