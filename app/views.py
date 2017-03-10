from app import app

@app.route('/')
@app.route('/index')
def index():
	return '''
<html>
        <head>
                <title>Test</title>
        </head>
        <body>
                <h1>TEST</h1>
        </body>
</html>
'''
