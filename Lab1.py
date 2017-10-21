from bottle import *#route, run, request
from collections import OrderedDict
import re
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import json
from string import Template

with open("client_secrets.json") as json_file:
	client_secrets = json.load(json_file)
	CLIENT_ID = client_secrets["web"]["client_id"]
	CLIENT_SECRET = client_secrets["web"]["client_secret"]
	SCOPE = client_secrets["web"]["auth_uri"]
	REDIRECT_URI = client_secrets["web"]["redirect_uris"][0]
	GOOGLE_SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'


#maintain across sessions:
#map search history to user individual dict
#10 most recently searched (stack?)

dict = {}
logged_in = 'Login'
user_email = ''

@route('/', 'GET')

def main():
#CSS formatting for the query page
    sign_in = '''
	<div align = "right">
	<form action = "/login" method = "get">
        <input id = "signin" type = "submit" value = "Sign In">
        </form>
	</div>
	'''
    sign_out = '''
	<div align = "right">
	<h3>Welcome, $user_email</h3>
	<form action = "/logout" method = "get">
        <input id = "signin" type = "submit" value = "Sign Out">
        </form>
	</div>
	'''
    sign_out = Template(sign_out).safe_substitute(user_email = user_email)
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
	#signin {
        width: 150px;
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
	if logged_in == 'Logout':
	        return sign_out, f, '\n'.join(history)
	else:
		return sign_in, f
    else:
	if logged_in == 'Logout':
		return sign_out, f
	else:
        	return sign_in, f


@route('/login', 'GET')

def login():
	global logged_in
	if logged_in == "Login":
		flow = flow_from_clientsecrets("client_secrets.json",scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri = "http://localhost:8080/redirect")
		uri = flow.step1_get_authorize_url()
		redirect(str(uri))
	else:
		logout()


@route('/redirect')
def redirect_page():
	global logged_in
	global user_email
	global token
	global http
	code = request.query.get('code','')

	flow = OAuth2WebServerFlow(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, scope = GOOGLE_SCOPE, redirect_uri = REDIRECT_URI)
	credentials = flow.step2_exchange(code)
	token = credentials.id_token['sub']

	http = httplib2.Http()
	http = credentials.authorize(http)

	users_service = build('oauth2', 'v2', http=http)
	user_document = users_service.userinfo().get().execute()
	user_email = user_document['email']
	#for i in user_document:
	#	print i, user_document[i]
	logged_in = 'Logout'
	return main()


@route('/logout', method='GET')
def logout():
	global logged_in
	logged_in = 'Login'
	user_email = ''
	redirect("https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080")
	return main()


@route('/search', method='GET')
def search():
    global logged_in
    string = request.query['keywords']
    string = re.sub(r'[^\w\s]','',string)   #filter punctuation
    l = string.lower().split()              #split by whitespaces
    cur = OrderedDict()
    updateHistory(l,cur)
    if logged_in == 'Logout':
    	updateHistory(l,dict)
    
    back = '<br><br><center><form action = "/"> <input id = "button" type = "submit" value = "Back"> </form></center>'
    #CSS formatting for results page
    sign_in = '''
	<div align = "right">
	<form action = "/login" method = "get">
        <input id = "signin" type = "submit" value = "Sign In">
        </form>
	</div>
	'''
    sign_out = '''
	<div align = "right">
	<h3>Welcome, $user_email</h3>
	<form action = "/logout" method = "get">
        <input id = "signin" type = "submit" value = "Sign Out">
        </form>
	</div>
	'''
    sign_out = Template(sign_out).safe_substitute(user_email = user_email)
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
            width: 70px;
            font-size: 20px;
            }
	    #signin {
            width: 150px;
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
        string = '''
		<center>
		<br><br><br>
		<br><br><br>
		<br><br><br> 
		Search query: ''' +string+ '''</center>'''
	if logged_in == "Logout":
	        return sign_out, string, out, '\n'.join(results), back
	else:
	        return sign_in, string, out, '\n'.join(results), back
    else:
        string = '''
		<style>
	        #signin {
	        width: 150px;
		font-size: 20px;
		}
		</style>
		<center>
		<br><br><br>
		<br><br><br>
		<br><br><br>
		<style>
		#button {
		width: 70px;
		font-size: 20px;
		}
		</style>
		<body bgcolor = "#F0B27A">  Search query: ''' +string + '''</body></center>'''
	if logged_in == "Logout":
	        return sign_out, string, back
	else:
	        return sign_in, string, back

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
