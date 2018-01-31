# slurm_handler


* users would need to create two dictionaries:
    * one would hold resources
    * the other would hold the inputs to their programs

**single file example with no iterables**

```python
from slurm_handler import JobSubmitter

# here the shown keys are required
resources = {"mem":2, "cores":2, "time": "0-00:01:00", "ngpu":0}

# however the keys for the inputs can be arbitrary, the first key and value pair
# must be the information for the file you want to run
call_items = {"key_1": "/mnt/bucket/people/yaraujjo/test.sh", "any thing": 3}

# where you want to write the file to
# and what the name of the sbatch file should be
sbatch_name = "sbatch_test.sh"
submit_dir = "/some/path/here"

# create the job submission object
jobs = JobSubmitter(call_items, resources, submit_dir, sbatch_name, "bash")

# submit the jobs
res = jobs.run()
```

**single file example with iterables**
```python
import numpy as np
from slurm_handler import JobSubmitter, Iterator

# slurm resources to request per job
resources = {"mem":2, "cores":2, "time": "0-00:01:00", "ngpu":0}

# template for what you script accepts, here test.sh takes in
# seed and alpha arguments, and test.sh is the script that will be called
call_items = {"key1": "/mnt/bucket/people/yaraujjo/test.sh",
              "seeds": "{seed}","alpha": "{alpha}"}

# values to iterate over per input argument that accepts them
iterables = {"seed":np.arange(10, 13), "alpha": [2,3,4]}

# name of the script to run
sbatch_name = "sbatch_test.sh"

# directory to hold the slurm file
submit_dir = "/mnt/bucket/people/yaraujjo/"

# create job submission object
jobs = JobSubmitter(call_items, resources, submit_dir, sbatch_name, "bash")

# create the iterator and pass in the job object plus your iterables
jobs_iter = Iterator(jobs, iterables)
jobs_iter.run()
```
