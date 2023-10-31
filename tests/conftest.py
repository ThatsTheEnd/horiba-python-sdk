# pylint: skip-file

import os
import time
import pytest
import subprocess
import logging


@pytest.fixture(scope="session", autouse=True)
def start_icl():
    if os.environ.get("HAS_HARDWARE") == "true":
        try:
            subprocess.run(
                ["C:\\Program Files\\Horiba Scientific\\SDK\\icl.exe"], check=True
            )
            time.sleep(0.5)
        except subprocess.CalledProcessError:
            logging.error("Failed to start ACL software.")
