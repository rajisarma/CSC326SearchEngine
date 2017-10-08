from bottle import route, run, request
from collections import OrderedDict
import re
dict = {}

@route('/')
def query():
#CSS formatting for the query page
    f ='''
        <br><br><br>
        <br><br><br>
        <br><br><br>
        <style>
        table {
        border-collapse: collapse;
        border: 1px solid black;
        }
        th, td {
        padding: 10px;
        }
        #searchbar {
        font-size: 30px;
        width: 600px;
        }
        #button {
        width: 85px;
        font-size: 20px;
        }
        </style>
        <body bgcolor = "#F0B27A">
        <center>
        <img src = "https://images.gr-assets.com/photos/1507480997p8/3630322.jpg" alt = "logo.gif" style = "width:506px;height:197px;background-color:#F0B27A;"/>
        <br> <br>
        <form action = "/search" method = "get">
        <input id = "searchbar" name = "keywords" type = "text">
        <input id = "button" type = "submit" value = "Search">
        <br>
        </form>
        </center>
        '''
    if bool(dict):
        i=0
        history = ['<center><br><br><b>Search History:</b><br><br><table id = "history">']
        history.append('<tr><td><b> Word </b></td>')
        history.append('<td><b> Count </b></td></tr>')
        for k in sorted(dict,key=dict.get,reverse=True):	#display top 20 searches on query page
            if i<20:
                history.append('<tr><td align="center"> %s </td>' % k)
                history.append('<td align="center"> %d </td></tr>' % dict[k])
                i += 1
        history.append('</table></center>')
        return f, '\n'.join(history)
    else:
        return f

@route('/search', method='GET')
def search():
    string = request.query['keywords']
    string = re.sub(r'[^\w\s]','',string)   #filter punctuation
    l = string.lower().split()              #split by whitespaces
    cur = OrderedDict()
    updateHistory(l,cur)
    updateHistory(l,dict)
    
    back = '<br><br><center><form action = "/"> <input id = "button" type = "submit" value = "Back"> </form></center>'
    #CSS formatting for results page
    if len(l)>1:
        results = ['''
            <center>
            <style>
            table {
                border-collapse: collapse;
                border: 1px solid black; 
            }
            th, td {
            padding: 10px;
            }
            #button {
            width: 60px;
            font-size: 20px;
            }
            </style>
            <br><b>Results:</b><br><br>
            <body bgcolor = "#F0B27A">
            <table id = "results">
            ''']
        out = '<center><br><br> Number of words in search phrase: '+str(len(l))+'</center>'
        results.append('<tr><td><b> Word </b></td>')
        results.append('<td><b> Count </b></td></tr>')
        for k in cur:	#display results table
            results.append('<tr><td align="center"> %s </td>' % k)
            results.append('<td align="center"> %d </td></tr>' % cur[k])
        results.append('</table></center>')
        string = '<center><br><br><br><br><br><br><br><br><br>'+string+'</center>'
        return string, out, '\n'.join(results), back
    else:
        string = '<center><br><br><br><br><br><br><br><br><br><body bgcolor = "#F0B27A">'+string + '</body></center>'
        return string, back

def updateHistory(l,dict):
#inputs: a list to process and a dictionary
#checks if each string in the list exists in the dictionary
#if yes: increments its count, if no: adds it to the dictionary
    for i in l:
        if not dict.get(i):
            dict[i] = 1
        else:
            dict[i] += 1

#run localhost
run(host='localhost', port=8080, debug=True)
