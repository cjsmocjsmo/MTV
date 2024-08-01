import argparse
import os
import subprocess
import utils
from dotenv import load_dotenv

CWD = os.getcwd()

def install():
    load_dotenv()
    
    print("Checking software dependencies")
    software = utils.SoftwareCheck()
    if not software.run_checks():
        print("Some checks failed.")
        os._exit(1)

    print("Checking paths")
    paths = utils.PathChecks()
    if not paths.run_checks():
        print("Some paths are missing.")
        os._exit(1)

    print("Stopping systemd service")
    sysd = utils.SystemdSetup(CWD)
    if sysd.service_file_check():
        sysd.stop_systemd_service()

    print("Building software")
    builder = utils.BuildSoftware(CWD)
    builder.clone_or_pull_build_setup()
    builder.copy_setup_binary()
    builder.clone_or_pull_build_mtv_server()
    builder.copy_mtvserverrust_binary()

    print("Starting Systemd service")
    if not sysd.service_file_check():
        sysd.copy_systemd_service_file()
        sysd.reload_systemd_service()
        sysd.enable_systemd_service()
        sysd.start_systemd_service()
    else:
        sysd.reload_systemd_service()
        sysd.start_systemd_service()

    if not os.path.exists("/tmp/mpvsocket"):
        print("Creating mpvsocket")
        subprocess.run(["sudo", "mkfifo", "/tmp/mpvsocket"])

def uninstall():
    sysd = utils.SystemdSetup(CWD)
    if sysd.service_file_check():
        sysd.stop_systemd_service()
        print("Disabling mtvserverrust service")
        subprocess.run(["sudo", "systemctl", "disable", "mtvserverrust.service"])
        print("Removing mtvserverrust service file")
        subprocess.run(["sudo", "rm", sysd.service_file_path])
        sysd.reload_systemd_service()
    
    if os.path.exists("/usr/bin/mtvserverrust"):
        print("Removing mtvserverrust binary")
        subprocess.run(["sudo", "rm", "/usr/bin/mtvserverrust"])

    if os.path.exists("/usr/bin/mtvsetup"):
        print("Removing mtvsetup binary")
        subprocess.run(["sudo", "rm", "/usr/bin/mtvsetup"])
    
    if os.path.exists("/usr/share/MTV"):
        print("Removing MTV directory")
        subprocess.run(["sudo", "rm", "-rf", "/usr/share/MTV"])

    if os.path.exists("/tmp/mpvsocket"):
        print("Removing mpvsocket")
        subprocess.run(["sudo", "rm", "/tmp/mpvsocket"])

    print("MTV has been uninstalled.\nYou can now remove this directory.")

def update():
    pass

def main():
    parser = argparse.ArgumentParser(description="Manage MTV installation.")
    parser.add_argument("operation", choices=["install", "update", "uninstall"], help="Operation to perform")

    args = parser.parse_args()

    if args.operation == "install":
        install()
    elif args.operation == "update":
        update()
    elif args.operation == "uninstall":
        uninstall()

if __name__ == "__main__":
    load_dotenv()
    main()