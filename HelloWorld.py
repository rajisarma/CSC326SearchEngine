from bottle import route, run, request
dict = {}

@route('/')
def hello():
	#s = '<b><i>Hello World</b></i> <br> <br>'
    f ='''
        <form action = "/search" method = "get">
        <input name = "keywords" type = "text">
        <br> <b>
        <input type = "submit" value = "Search">
        </b> <br>
        </form>
        '''
    history = ['<table id = "History">']
    for k in sorted(dict,key=dict.get,reverse=True):
        history.append('<tr><td> %s </td>' % k)
        history.append('<td> %d </td></tr>' % dict[k])
    history.append('</table>')
    return f, '\n'.join(history)

@route('/search', method='GET')
def search():
    string = request.query['keywords']
    l = string.lower().split()
    cur = {}
    updateHistory(l,cur)
    updateHistory(l,dict)
    results = ['<table id = "Results">']
    for k in sorted(cur,key=cur.get,reverse=True):
        results.append('<tr><td> %s </td>' % k)
        results.append('<td> %d </td></tr>' % cur[k])
    results.append('</table>')
    return string, '\n'.join(results)

def updateHistory(l,dict):
    for i in l:
        if not dict.get(i):
            dict[i] = 1
        else:
            dict[i] += 1


run(host='localhost', port=8080, debug=True)
