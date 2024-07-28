import os
import subprocess
import utils
from dotenv import load_dotenv



class BuildSoftware:
    def __init__(self):
        self.CWD = os.getcwd() # assuming /home/pi/MTV
        self.setupdir = self.CWD + "/SetUp/"
        os.mkdir(self.setupdir)
        self.mtvdir = self.CWD + "/MTV/"
        os.mkdir(self.mtvdir)

    def clone_setup(self):
        subprocess.run(
            [
                "git", 
                "clone", 
                "https://github.com/cjsmocjsmo/mtvsetup.git", 
                self.setupdir,
            ])
        
    def clone_mtv_server(self):
        subprocess.run(
            [
                "git", 
                "clone", 
                "https://github.com/cjsmocjsmo/mtvserverrust.git",
                self.mtvdir,
            ])
        
    def build_setup(self):
        os.chdir(self.setupdir)
        subprocess.run(["cargo", "build", "--release"])
        os.chdir(self.CWD)

    def build_mtv_server(self):
        os.chdir(self.mtvdir)
        subprocess.run(["cargo", "build", "--release"])
        os.chdir(self.CWD)

if __name__ == "__main__":
    load_dotenv()
    software = utils.SoftwareCheck()
    if not software.run_checks():
        print("Some checks failed.")
        os._exit(1)
    paths = utils.PathChecks()
    if not paths.run_checks():
        print("Some paths are missing.")
        os._exit(1)
    builder = BuildSoftware()
    builder.clone_setup()
    builder.clone_mtv_server()
    