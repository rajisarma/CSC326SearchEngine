from bottle import route, run, request
from collections import OrderedDict
import re
dict = {}

@route('/')
def query():
#CSS formatting for the query page
	f ='''
	<HTML>
	<body>
	<br><br><br>
	<br><br><br>
	<br><br><br>
	Crawler
	<br>
	Testing
	<br>
	for search engine
	<br>
	Lab1
	<br> 
	Programming Languages CSC326
        <br>
        <br>
        <a href="/search">Second Page</a>
	<a href="/third">3rd Page</a>
	<a href="/fourth">4th Page</a>
	<a href="/fifth">5th Page</a>
	</body>
	</HTML>
        '''
	return f

@route('/search', method='GET')
def search():
	string = '''
	<HTML>
	<body>
	<br><br><br>
	<br><br><br>
	<br><br><br>
	Testing
	<br>
	testing
	<br>
	Computer
	</body>
	</HTML>
	'''
        return string

@route('/third', method='GET')
def search():
	string = '''
	<HTML>
	<body>
	<br><br><br>
	<br><br><br>
	<br><br><br>
	Testing
	<br>
	Language
	<br>
	Computers
	</body>
	</HTML>
	'''
        return string

@route('/fourth', method='GET')
def search():
	string = '''
	<HTML>
	<body>
	<br><br><br>
	<br><br><br>
	<br><br><br>
	hello
	<br>
	testing
	<br>
	world
	</body>
	</HTML>
	'''
        return string

@route('/fifth', method='GET')
def search():
	string = '''
	<HTML>
	<body>
	<br><br><br>
	<br><br><br>
	<br><br><br>
	lab
	<br>
	search
	<br>
	engine
	</body>
	</HTML>
	'''
        return string

#run localhost
run(host='localhost', port=8080, debug=True)
