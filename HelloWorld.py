from bottle import route, run, request
from collections import OrderedDict

dict = {}

@route('/')
def hello():
    f ='''
        <form action = "/search" method = "get">
        <input name = "keywords" type = "text">
        <br> <b>
        <input type = "submit" value = "Search">
        </b> <br>
        </form>
        '''
    if bool(dict):
        i=0
        history = ['<table id = "history">']
        history.append('<tr><td><b> Word </b></td>')
        history.append('<td><b> Count </b></td></tr>')
        for k in sorted(dict,key=dict.get,reverse=True):
            if i<20:
                history.append('<tr><td> %s </td>' % k)
                history.append('<td> %d </td></tr>' % dict[k])
                i += 1
        history.append('</table>')
        return f, '\n'.join(history)
    else:
        return f

@route('/search', method='GET')
def search():
    string = request.query['keywords']
    l = string.lower().split()
    cur = OrderedDict()
    updateHistory(l,cur)
    updateHistory(l,dict)
    if len(cur)>1:
        results = ['<table id = "results">']
        results.append('<tr><td><b> Word </b></td>')
        results.append('<td><b> Count </b></td></tr>')
        for k in cur:
            results.append('<tr><td> %s </td>' % k)
            results.append('<td> %d </td></tr>' % cur[k])
        results.append('</table>')
        return string, '\n'.join(results)
    else:
        return string

def updateHistory(l,dict):
    for i in l:
        if not dict.get(i):
            dict[i] = 1
        else:
            dict[i] += 1


run(host='localhost', port=8080, debug=True)
