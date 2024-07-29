import os
import shutil
import subprocess


class SoftwareCheck:
    def mpv_check(self):
        try:
            subprocess.check_output(["apt", "list", "mpv"])
            return True
        except subprocess.CalledProcessError:
            print("MPV is not installed.")
            return False
        
    def mpvctl_check(self):
        foo = os.path.exists("/usr/bin/mpvctl") 
        if not foo:
            print("MPVCTL is not installed.")
        return foo

    def rust_check(self):
        try:
            subprocess.check_output(["rustc", "--version"])
            return True
        except subprocess.CalledProcessError:
            print("Rust is not installed.")
            return False
        
    def run_checks(self):
        mpv = self.mpv_check()
        mpvctl = self.mpvctl_check()
        rust = self.rust_check()
        if mpv and mpvctl and rust:
            return True
        else:
            return False
        
class PathChecks:
    def __init__(self):
        if not os.path.isdir("/usr/share/MTV"):
            os.mkdir("/usr/share/MTV")

    def dbpath_check(self):
        if os.path.exists(os.getenv("MTV_DB_PATH")):
            return True
        else:
            print("Database path is missing.")
            return False
    
    def staticpath_check(self):
        if os.path.exists(os.getenv("MTV_STATIC_PATH")):
            return True
        else:
            print("Static path is missing. Creating Dir")
            os.mkdir(os.getenv("MTV_STATIC_PATH"))
            if os.path.exists(os.getenv("MTV_STATIC_PATH")):
                return True
            else:
                return False
    
    def tvpath_check(self):
        if os.path.exists(os.getenv("MTV_TV_PATH")):
            return True
        else:
            print("TV path is missing.")
            return False
    
    def setuppath_check(self):
        if os.path.exists(os.getenv("MTV_SETUP_PATH")):
            return True
        else:
            print("Setup path is missing.")
            return
    
    def mtvpath_check(self):
        if os.path.exists(os.getenv("MTV_MTV_PATH")):
            return True
        else:
            print("MTV path is missing.")
            return False
    
    def moviespath_check(self):
        if os.path.exists(os.getenv("MTV_MOVIES_PATH")):
            return True
        else:
            print("Movies path is missing.")
            return False
    
    def posterpath_check(self):
        if os.path.exists(os.getenv("MTV_POSTER_PATH")):
            return True
        else:
            print("Poster path is missing.")
            return False

    def thumbnailpath_check(self):
        if os.path.exists(os.getenv("MTV_THUMBNAIL_PATH")):
            return True
        else:
            os.mkdir(os.getenv("MTV_THUMBNAIL_PATH"))
            if os.path.exists(os.getenv("MTV_THUMBNAIL_PATH")):
                return True
            else:
                print("Thumbnail path is missing.")
                return False
    
    def run_checks(self):
        dbpath = self.dbpath_check()
        staticpath = self.staticpath_check()
        tvpath = self.tvpath_check()
        setuppath = self.setuppath_check()
        mtvpath = self.mtvpath_check()
        moviespath = self.moviespath_check()
        posterpath = self.posterpath_check()
        thumbnailpath = self.thumbnailpath_check()
        if dbpath and staticpath and tvpath and setuppath and mtvpath and moviespath and posterpath and thumbnailpath:
            return True
        else:
            return False
        
class BuildSoftware:
    def __init__(self, CWD):
        self.CWD = CWD
        # self.CWD = os.getcwd() # assuming /home/pi/MTV  
        self.setupdir = self.CWD + "/SetUp/"
        self.mtvdir = self.CWD + "/MTV/"

    def clone_or_pull_build_setup(self):
        foo = os.path.exists(self.setupdir)
        if foo:
            print(self.setupdir)
            os.chdir(self.setupdir)
            subprocess.run(["git", "pull"])
            subprocess.run(["cargo", "build", "--release"])
            os.chdir(self.CWD)
        else:
            os.makedirs(self.setupdir)
            subprocess.run(
                [
                    "git", 
                    "clone", 
                    "https://github.com/cjsmocjsmo/mtvsetup.git", 
                    self.setupdir,
                ])
            os.chdir(self.setupdir)
            subprocess.run(["cargo", "build", "--release"])
            os.chdir(self.CWD)
        
    def clone_or_pull_build_mtv_server(self):
        bar = os.path.exists(self.mtvdir)
        if bar:
            print(self.mtvdir)
            os.chdir(self.mtvdir)
            subprocess.run(["git", "pull"])
            subprocess.run(["cargo", "build", "--release"])
            os.chdir(self.CWD)
        else:
            os.makedirs(self.mtvdir)
            subprocess.run(
                [
                    "git", 
                    "clone", 
                    "https://github.com/cjsmocjsmo/mtvserverrust.git",
                    self.mtvdir,
                ])
            os.chdir(self.mtvdir)
            subprocess.run(["cargo", "build", "--release"])
            os.chdir(self.CWD)

    def copy_setup_binary(self):
        if os.path.exists("/usr/bin/mtvsetup"):
            subprocess.run(["sudo", "rm", "-f","/usr/bin/mtvsetup"])
        new_loc_dir = "/usr/bin/"
        binary_loc = "".join((self.setupdir, "target/release/mtvsetup"))
        # shutil.copy(binary_loc, new_loc_dir)
        subprocess.run(["sudo", "cp", "-pvr", binary_loc, new_loc_dir])

    def copy_mtvserverrust_binary(self):
        if os.path.exists("/usr/bin/mtvserver"):
            subprocess.run(["sudo", "rm", "-f","/usr/bin/mtvserver"])
        new_loc_dir = "/usr/bin/"
        binary_loc = "".join((self.mtvdir, "target/release/mtvserver"))
        # shutil.copy(binary_loc, new_loc_dir)
        subprocess.run(["sudo", "cp", "-pvr", binary_loc, new_loc_dir])