# example use case

* users would need to create two dictionaries: 
    * one would hold resources
    * the other would hold the inputs to their programs

**single file example with no iterables**

```python
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
