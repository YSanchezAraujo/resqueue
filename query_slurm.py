import subprocess

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
   
""" can use the above to check jobids, as a first use case, try
to check your jobs and count how many you have running, will somehow
have to limit it to only jobs queued up within slurm_handler
"""
