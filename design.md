# Design plan for this piece of software

* users would need to create two dictionaries: 
    * one would hold resources
    * the other would hold the inputs to their programs

**single file example with no iterables**

```python
# here the shown keys are required
resources = {"mem":2, "cores":2, "time": "0-00:01:00", "ngpu":0}

# however the keys for the inputs can be arbitrary
call_items = {"key_1": "/mnt/bucket/people/yaraujjo/test.sh", "any thing": 3}

"""the following will create the text that is written to file as an .sh file that
the last item, 'bash' means I'm calling a bash script. That bash script is the item
of call_items, and it's additionally taking in the parameter 3
"""
cmd = make_call_cmd(call_items, resources, "bash")

# now we write the file
name = "sbatch_test.sh"
path = "/some/path/here"
file_written = write(path, name, cmd)

# finally we call sbatch on the file 
out = command("sbatch {}".format(file_written))
```

**single file example with iterables**
