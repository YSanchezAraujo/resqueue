import subprocess

def shell(cmd_split):
    process = subprocess.Popen(cmd_split, stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("utf-8").split("\n")
