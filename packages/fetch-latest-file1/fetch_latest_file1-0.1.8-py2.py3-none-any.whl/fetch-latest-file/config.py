import atexit
import click
import logging
from pathlib import Path
import sys
import json
import os

class Config(object):
    def __init__(self):
        super().__init__()
        self.settings = json.loads(Path(os.path.expanduser("~/.fetch_latest_file")).read_text())
        self.host = None

        def cleanup():
            pass

        atexit.register(cleanup)

    def setup_logging(self):
        FORMAT = '[%(levelname)s] %(asctime)s %(message)s'
        formatter = logging.Formatter(FORMAT)
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('')  # root handler
        self.logger.setLevel(self.log_level)

        stdout_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(stdout_handler)
        stdout_handler.setFormatter(formatter)


pass_config = click.make_pass_decorator(Config, ensure=True)
