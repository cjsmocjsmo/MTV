import os
import utils
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    CWD = os.getcwd()

    software = utils.SoftwareCheck()
    if not software.run_checks():
        print("Some checks failed.")
        os._exit(1)

    paths = utils.PathChecks()
    if not paths.run_checks():
        print("Some paths are missing.")
        os._exit(1)

    sysd = utils.SystemdSetup(CWD)
    if sysd.service_file_check():
        sysd.stop_systemd_service()

    builder = utils.BuildSoftware(CWD)
    builder.clone_or_pull_build_setup()
    builder.copy_setup_binary()
    builder.clone_or_pull_build_mtv_server()
    builder.copy_mtvserverrust_binary()

    if not sysd.service_file_check():
        sysd.copy_systemd_service_file()
        sysd.reload_systemd_service()
        sysd.enable_systemd_service()
        sysd.start_systemd_service()
    else:
        sysd.reload_systemd_service()
        sysd.start_systemd_service()

    