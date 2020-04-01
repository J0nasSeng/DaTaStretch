from datastretch.pipeline import Pipeline
from datastretch.pipeline import Stage
from pipeline_tests.Output import Output
from pipeline_tests.Loaders import *
from pipeline_tests.Processors import *

loader1 = LoaderSource1()
loader2 = LoaderSource2()
loader3 = LoaderSource3()

pt1 = ProcessingTask1()
pt2 = ProcessingTask2()

out = Output()

# pt1 has to wait for loader1:
pt1.dependency(loader1)

# pt2 has to wait for loader2 and loader3
pt2.dependency(loader2, loader3)

# output has to wait for both processing-objects
out.dependency(pt1, pt2)

loader3.run_args('Our argument')

stage1, stage2, stage3 = Stage(), Stage(), Stage()

stage1.add(loader1, loader2, loader3)

stage2.add(pt1, pt2)

stage3.add(out)

pipeline = Pipeline()
pipeline.add(stage1, stage2, stage3)

pipeline.compile()
# you can plot those if you want to:
# pipeline.plot('task')
# pipeline.plot('execution')
if __name__ == '__main__':
    pipeline.run()
