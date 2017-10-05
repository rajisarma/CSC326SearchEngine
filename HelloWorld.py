from bottle import route, run, request

@route('/')
def hello():
	s = '<b><i>Hello World</b></i> <br> <br>'
	f = '<form action = "/search" method = "get" > <input name = "keywords" type = "text"> <br> <b> <input type = "submit" value = "Search"> </b> <br> </form>'
	return s,f

@route('/search', method='GET')
def search():
	string = request.query['keywords']
	print string
	return "success: "+ string


run(host='localhost', port=8080, debug=True)
