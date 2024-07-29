import os
# import subprocess
import utils
from dotenv import load_dotenv

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
    builder = utils.BuildSoftware()
    builder.clone_or_pull_setup
    builder.build_setup()
    builder.clone_or_pull_mtv_server()
    builder.build_mtv_server()
    