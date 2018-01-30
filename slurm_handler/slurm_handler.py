import os
import time
import subprocess
import itertools

def reformat_input(files, sep=" "):
    """files, a list of files or a string of many files
    each seperated by a space
    """
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
        "#SBATCH --time={time}", "#SBATCH --gres=gpu:{ngpu}\n"
    ]
    for key in ["mem", "cores", "time", "ngpu"]:
        if key not in resource.keys():
            raise ValueError(
                "resource dictionary should have the key: {}".format(key)
            )
    scmd = " ".join(script_call + fmt_place_holders).format(**iter_items)
    return "\n".join(cmdstr + [scmd]).format(**resource)

def _make_product(items):
    """for_prod: list of list or list of tuples, each
    list/tuple in the other list is a set of things  you
    want to iterate over
    """
    yield from itertools.product(*items)

def iterate_product(for_prod, func):
    """for_prod: list of list or list of tuples, each
    list/tuple in the other list is a set of things  you
    want to iterate over
    func: a function that accepts a number of argumets equal
    to the number of inner lists/tuples in for_prod
    """
    for val in _make_product(for_prod):
        func(val)

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
    time.sleep(1)
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

class JobSubmitter(object):
    """ initial class object that will take in all of the
    required information to do the work of creating files,
    submitting jobs, etc.
    """
    def __init__(self, call_items, resources, submit_dir, sbatch_name, prog_type=None, iter_dir=None):
        self.call_items = call_items
        self.resources = resources
        self.submit_dir = submit_dir
        self.sbatch_name = sbatch_name
        self.prog_type = prog_type

    def _write(self, text):
        split_name = self.sbatch_name.split(".")
        if split_name[-1] != "sh":
            raise Exception(
                "make sure that your file ends with .sh (e.g test.sh)"
            )
        if self.iter_dir is not None:
            sbatch_dir_name = self.iter_dir
        else:
            sbatch_dir_name = '_'.join([i for i in split_name[:-1]])
        if "~" in self.submit_dir:
            raise Exception(
                "~ in place of the home path is not allowed please provide the full path"
            )
        write_dir = os.path.join(self.submit_dir, sbatch_dir_name)
        if not os.path.isdir(write_dir):
            os.makedirs(write_dir)
            os.chdir(write_dir)
        else:
            raise FileExistsError(
                "{} exists".format(write_dir)
            )
        file_path = os.path.join(write_dir, self.sbatch_name)
        with open(file_path, "w") as writing:
            writing.write(text)
        self.file_written = file_path
        return file_path  

    def run(self):
        cmd = make_call_cmd(self.call_items, self.resources, self.prog_type)
        file_written = self._write(cmd)
        sbatch_res = command("sbatch {}".format(file_written))
        slurm_handle(sbatch_res)
        return sbatch_res 

class Iterator(object):
    """ class to be used when the inputs to the computation file
    expects an iteration over them. The input to this class should be a
    JobSubmitter object
    """
    def __init__(self, jobsub, iterables):
        self.jobsub = jobsub
        self.iterables = iterables

    def run_each(self, iter_vals):
        cur_dir_name = '_'.join(self.jobsub.sbatch_name.split(".")[:-1])
        iter_dir_name = cur_dir_name + "_{}_{}".format(*iter_vals)
        self.jobsub.iter_dir = iter_dir_name
        iter_dict = {}
        for idx, key in enumerate(self.iterables.keys()):
            iter_dict[key] = iter_vals[idx]
        call_values = ' '.join(self.jobsub.call_items.values()).format(**iter_dict).split()
        call_values.insert(0, self.jobsub.call_items.values()[0])
        for idx, key in enumerate(self.jobsub.call_items.keys()):
            self.jobsub.call_items[key] = call_values[idx]
        self.jobsub.run() 
    
    def run(self):
        product = iterate_product(iterables.values(), self.run_each)
     


