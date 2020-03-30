## exceptions
In this part all exceptions defined by the `Pipeline`-framework are explained.

### AssignmentError
This error is raised if for some constant attribute in an object a trial is made to change its value.
To avoid this you should use copies of constant variables. To see which variables are constant, search the documentation.

### PipelineRuntimeError:
This error is raised if the execution of one or more tasks in the pipeline fails. The reasons for this can be:
1. a non-task-object is passed in the pipeline

### CompilationError
This error is raised if it is not possible to build the execution graph from the task graph. The task graph contains cycles
which are not allowed in a pipeline.
