import subprocess
from collections import Counter

def command(cmd, sep=" "):
    """cmd: string or list, the command you want to execute,
    examples: "ls -a", ["ls", "-a"]
    sep: string, how you want to split the string into a list
    if the seperator between tokens in the commands is not a space
    """
    if isinstance(cmd, str):
        cmd = cmd.split(sep)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8").split("\n")

def slurm_handle(piped_input):
    """piped_input: list, this is the output from the command function
    intended for squeue but maybe will be used for other commands
    keep in mind that this modifies the input inplace
    """
    for idx, line in enumerate(piped_input):
        piped_input[idx] = line.split()
    if not piped_input[-1]:
        del piped_input[-1]

def test_combine(cmd):
    """cmd: slurm command to be executed
    right now this is just a throw away function,
    it won't be used later on just getting ideas
    """
    info = command(cmd)
    slurm_handle(info)
    njobs = len(info) - 1
    return {"info":info, "njobs":njobs}
    
