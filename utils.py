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

def make_call_cmd(iter_items, resource, type_script):
    """iter_items: dict
    resource: dict, resources for sbatch call
    """
    script_dict = dict(R="Rscript --vanilla", py="python", sh="bash")
    if type_script not in script_dict.keys():
        raise ValueError(
            "type_script must be one of: {}".format(script_dict.keys())
        )
    script_call = [script_dict[type_script]]
    fmt_place_holders = ["{{{}}}".format(key) for key in iter_items.keys()]
    cmdstr = [
        "#!/bin/bash", "#SBATCH --mem={mem}G", "#SBATCH -c {cores}",
        "#SBATCH --time={time}",
    ]
    for key in ["mem", "cores", "time"]:
        if key not in resource.keys():
            raise ValueError(
                "resource dictionary should have the key: {}".format(key)
        )
    scmd = " ".join(script_call + fmt_place_holders).format(**iter_items)
    return "\n".join(cmdstr + [scmd]).format(**resource)
