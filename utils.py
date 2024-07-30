import os
# import shutil
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
            subprocess.run(["sudo", "mkdir", "/usr/share/MTV"])

    def dbpath_check(self):
        if os.path.exists(os.getenv("MTV_DB_PATH")):
            return True
        else:
            print("Database path is missing.\nCreating mtv.db")
            with open(os.getenv("MTV_DB_PATH"), "w") as f:
                pass
            if os.path.exists(os.getenv("MTV_DB_PATH")):
                return True
            else:
                return False
    
    def staticpath_check(self):
        if os.path.exists(os.getenv("MTV_STATIC_PATH")):
            return True
        else:
            print("Static path is missing. Creating Dir")
            subprocess.run(["sudo", "mkdir", os.getenv("MTV_STATIC_PATH")])
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
            subprocess.run(["sudo", "mkdir", os.getenv("MTV_THUMBNAIL_PATH")])
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
                ]
            )
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
                ]
            )
            os.chdir(self.mtvdir)
            subprocess.run(["cargo", "build", "--release"])
            os.chdir(self.CWD)

    def copy_setup_binary(self):
        if os.path.exists("/usr/bin/mtvsetup"):
            subprocess.run(["sudo", "rm", "-f","/usr/bin/mtvsetup"])
        new_loc_dir = "/usr/bin/"
        binary_loc = "".join((self.setupdir, "target/release/mtvsetup"))
        subprocess.run(["sudo", "cp", "-pvr", binary_loc, new_loc_dir])

    def copy_mtvserverrust_binary(self):
        if os.path.exists("/usr/bin/mtvserver"):
            subprocess.run(["sudo", "rm", "-f","/usr/bin/mtvserverrust"])
        new_loc_dir = "/usr/bin/"
        binary_loc = "".join((self.mtvdir, "target/release/mtvserverrust"))
        subprocess.run(["sudo", "cp", "-pvr", binary_loc, new_loc_dir])

class SystemdSetup:
    def __init__(self, CWD):
        self.CWD = CWD
        self.sysd_dir = "/etc/systemd/system/"
        self.service_file_path= "".join((self.sysd_dir, "mtvserverrust.service"))
        self.serv_file_loc = "/".join((self.CWD, "mtvserverrust.service"))
        
    def service_file_check(self):
        if os.path.exists(self.service_file_path):
            return True
        else:
            return False

    def copy_systemd_service_file(self):
        subprocess.run(
            [
                "sudo", 
                "cp", 
                "-pvr", 
                self.serv_file_loc, 
                self.service_file_path,
            ]
        )

    def enable_systemd_service(self):
        subprocess.run(
            [
                "sudo", 
                "systemctl", 
                "enable", 
                "mtvserverrust.service",
            ]
        )

    def start_systemd_service(self):
        subprocess.run(
            [
                "sudo", 
                "systemctl", 
                "start", 
                "mtvserverrust.service",
            ]
        )

    def stop_systemd_service(self):
        subprocess.run(
            [
                "sudo", 
                "systemctl", 
                "stop", 
                "mtvserverrust.service",
            ]
        )

    def reload_systemd_service(self):
        subprocess.run(
            [
                "sudo", 
                "systemctl", 
                "daemon-reload",
            ]
        )
    