#!/usr/bin/env python3

import os
import sys
import logging

PROJECT_DIR = "/var/www/catalog"
activate_filename = 'activate_this.py'
logging.basicConfig(stream=sys.stderr)

activate_this = os.path.join(PROJECT_DIR, 'venv', 'bin', activate_filename)
with open(activate_this) as activate_file:
    code = compile(activate_file.read(), activate_filename, 'exec')
    exec(code)
sys.path.append(PROJECT_DIR)

from main import app as application
