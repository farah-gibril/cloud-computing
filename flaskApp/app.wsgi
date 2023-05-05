#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, '/home/ubuntu/myapp')

from myapp import app as application
application.secret_key = 'mysecretkey'