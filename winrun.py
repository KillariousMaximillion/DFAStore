'''
This is a DEVElOPMENT ONLY script
Use WSGI to run application in production on a production server.
See runp.fcgi file for one possible solution
'''
#!flask/bin/python
from app import app

app.run(debug=True)