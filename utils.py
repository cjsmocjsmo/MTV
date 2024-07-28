import subprocess
import os

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
        return os.path.exists(os.getenv("MTV_DB_PATH"))
    
    def staticpath_check(self):
        return os.path.exists(os.getenv("MTV_STATIC_PATH"))
    
    def tvpath_check(self):
        return os.path.exists(os.getenv("MTV_TV_PATH"))
    
    def setuppath_check(self):
        return os.path.exists(os.getenv("MTV_SETUP_PATH"))
    
    def mtvpath_check(self):
        return os.path.exists(os.getenv("MTV_MTV_PATH"))
    
    def moviespath_check(self):
        return os.path.exists(os.getenv("MTV_MOVIES_PATH"))
    
    def posterpath_check(self):
        return os.path.exists(os.getenv("MTV_POSTER_PATH"))

    def thumbnailpath_check(self):
        return os.path.exists(os.getenv("MTV_THUMBNAIL_PATH"))
    
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