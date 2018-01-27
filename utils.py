import os

"""
next steps:
figure out the plan for the iterator, have it be
general enough so that it can handle cross products between
sets of iterables, and well as sets of lists of iterables
"""

def reformat_input(files, sep=" "):
    if isinstance(files, str):
        files = files.split(" ")
    out = sep.join(files)
    return '"{}"'.format(out)

#TODO: add sbatch GPU resources
def make_call_cmd(iter_items, resource, type_script=None):
    """iter_items: dict
    resource: dict, resources for sbatch call
    type_script: string, this will insert the command to
    the program you want to run
    """
    if type_script is None:
        print("WARNING, type_script is defaulting to bash"
              ", consider using a particular program call"
              " for example, type_script='python'")
        type_script = "bash"
    script_call = [type_script]
    fmt_place_holders = ["{{{}}}".format(key) for key in iter_items.keys()]
    cmdstr = [
        "#!/bin/bash\n", "#SBATCH --mem={mem}G", "#SBATCH -c {cores}",
        "#SBATCH --time={time}\n",
    ]
    for key in ["mem", "cores", "time"]:
        if key not in resource.keys():
            raise ValueError(
                "resource dictionary should have the key: {}".format(key)
            )
    scmd = " ".join(script_call + fmt_place_holders).format(**iter_items)
    return "\n".join(cmdstr + [scmd]).format(**resource)


def write(path, name, text):
    write_file = os.path.join(path, name)
    with open(write_file, "w") as writer:
        writer.write(text)
    return write_file


