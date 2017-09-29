from bottle import route, run, request
@route('/')
def hello():
	s = '<b><i>Hello World</b></i> <br> <br>'
	f = '<form action = "/search" method = "post" > <input name = "search" type = "search"> <br> <b> <input type = "submit" value = "Search"> </b> <br> </form>'
	return s,f

@route('/search', method='POST')
def search():
	string = request.forms.get('search')
	return "success: "+ string


run(host='localhost', port=8080, debug=True)
