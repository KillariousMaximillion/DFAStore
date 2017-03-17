###
# Production Script for running application on a production webserver.
###
#!flask/bin/python
import os

from flipflop import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()
