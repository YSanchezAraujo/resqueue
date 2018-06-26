import os
import subprocess

class Matlab(object):
    """ very preliminary, initial matlab class
    to support matlab computing
    """
    def __init__(self, matfile, cmd=None):
        self.matfile = matfile
        self.cmd = cmd
    
    def _file_exists(self):
        if not os.path.isfile(self.matfile):
            raise Exception("file cannot be found: matfile")

    def _add_prefix_suffix(self):
        """ method reads in the matlab script and makes it
        a function so that it can be called via the malab
        terminal command
        """
        with open(self.matfile, 'r') as mfile:
            matfile = mfile.read()
        self.prefix = "function[proxy]=resmat()\n"
        self.suffix = "\nend\n"
        self.mat_text = self.prefix + matfile + self.suffix
        new_path = os.path.join(os.path.dirname(self.matfile), "resmat.m")
        with open(new_path, 'w') as mfile:
            mfile.write(self.mat_text)
        self.edited_matfile = new_path

    def _mlabcmd(self):
        if self.cmd is None:
            self.cmd = "matlab -nodesktop -nojvm -nodisplay -r"
        self.cmd = self.cmd + " resmat();quit"
    
    def run(self):
        self._file_exists()
        self._add_prefix_suffix()
        self._mlabcmd()
        if os.getcwd() != os.path.dirname(self.edited_matfile):
            os.chdir(os.path.dirname(self.edited_matfile))
        process = subprocess.Popen(self.cmd.split(), stdout=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode("utf-8").split("\n")



    
