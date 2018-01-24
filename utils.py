import os
from subprocess import call

def reformat_input(files, sep=" "):
    outstr = '"'
    
    if isinstance(files, list):
        for idx, f in enumerate(files):
            if idx+1 != len(files):
                outstr += (f + sep)
            else:
                outstr += f
        outstr += '"'
        
    elif isinstance(files, str):
        flist = files.split(" ")
        for idx, f in enumerate(flist):
            if idx+1 != len(files):
                outstr += (f + sep)
            else:
                outstr += f
        outstr += '"'
        
    return outstr

def make_call_cmd(iter_items, resource, type_script):
    """iter_keys: dict inputs
    resource: dict, resources for sbatch call
    """
    script_dict = dict(R="Rscript --vanilla", py="python", sh="bash")
    
    if type_script not in script_dict.keys():
        raise ValueError("type_script must be one of :{}".format(script_dict.keys()))
        
    script_call = [script_dict[type_script]]
    fmt_place_holders = ["{{{}}}".format(key) for key in iter_items.keys()]
    cmdstr = ["#!/bin/bash", "#SBATCH --mem={mem}G", "#SBATCH -c {cores}", "#SBATCH --time={time}"]
    Scmd = " ".join(script_call + fmt_place_holders).format(**iter_items)
    cmd = cmdstr + [Scmd]
    return "\n".join(cmd).format(**resource)
