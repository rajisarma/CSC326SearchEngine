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

#for localhost
#MAIN = "http://localhost:8080/redirect"
#for AWS instance
MAIN = "http://0.0.0.0:80/redirect"

#for localhost:
#HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080"
HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://0.0.0.0:80"


#from json file, get values needed to start login process
with open("client_secrets.json") as json_file:
	client_secrets = json.load(json_file)
	CLIENT_ID = client_secrets["web"]["client_id"]
	CLIENT_SECRET = client_secrets["web"]["client_secret"]
	SCOPE = client_secrets["web"]["auth_uri"]
	REDIRECT_URI = client_secrets["web"]["redirect_uris"][0]
	GOOGLE_SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

cache = {}
dict = {}
last10 = []
logged_in = 'Login'
user_email = ''
user_name = ''
pic_link = ''


@route('/', 'GET')

def main():
#CSS formatting for the query page
#sign in button
    sign_in = '''
	<div align = "right">
	<form action = "/login" method = "get">
        <input id = "signin" type = "submit" value = "Sign In">
        </form>
	</div>
	'''
#sign out button (displays when user is logged in, along with user's google profile picture)
    sign_out = '''
	<div align = "right">
	<h3>Welcome, $user_name</h3>
	<img src = $pic_link alt = "profilepic" style = "width:100px;height:auto"/>	
	<br>
	<form action = "/logout" method = "get">
        <input id = "signin" type = "submit" value = "Sign Out">
        </form>
	</div>
	'''
    sign_out = Template(sign_out).safe_substitute(user_name = user_name, pic_link = pic_link)
#search bar and search button
    f ='''
        <br><br><br><br>
        <style>
        table {
        border-collapse: collapse;
        border: 1px solid black;
	display: inline-block;
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
#if most searched table contains values and user is logged in, display table
    if bool(dict) and logged_in == 'Logout':
        i=0
        history = ['<center><br><br><b>Search History:</b><br><br><table id = "history">']
        history.append('<tr><td align="center"><b> Word </b></td>')
        history.append('<td align="center"><b> Count </b></td></tr>')
        for k in sorted(dict,key=dict.get,reverse=True):	#display top 20 searches on query page
            if i<20:
                history.append('<tr><td align="center"> %s </td>' % k)
                history.append('<td align="center"> %d </td></tr>' % dict[k])
                i += 1
        history.append('</table><center>')

#if recent search table contains values and user is logged in, display table by printing list in reverse to put the most recently searched word first
	if len(last10)>0:
		recent = ['''
            <center>
            <style>
            table {
                border-collapse: collapse;
                border: 1px solid black;
		display: inline-block;
            }
            th, td {
            padding: 10px;
            }
            </style>
            <br><b>Most Recent Searches:</b><br><br>
            <body bgcolor = "#F0B27A">
            <table id = "recent">
            ''']
		recent.append('<tr><td align="center"><b> Word </b></td>')
		count = 0
		for q in reversed(last10):
			if count<10:
				recent.append('<tr><td align="center">%s</td>' %q)
				count += 1
		recent.append('</table></center>')

	if logged_in == 'Logout':
	        return sign_out, f, '\n'.join(history), '\n'.join(recent)
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
		flow = flow_from_clientsecrets("client_secrets.json",scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri = MAIN)
		uri = flow.step1_get_authorize_url()
		redirect(str(uri))
	else:
		logout()


@route('/redirect')
def redirect_page():
	global logged_in
	global user_email, user_name, pic_link, link
	global http
	global dict, last10
	code = request.query.get('code','')

	flow = OAuth2WebServerFlow(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, scope = GOOGLE_SCOPE, redirect_uri = REDIRECT_URI)
	credentials = flow.step2_exchange(code)
	token = credentials.id_token['sub']

	http = httplib2.Http()
	http = credentials.authorize(http)

	users_service = build('oauth2', 'v2', http=http)
	user_document = users_service.userinfo().get().execute()
	user_email = user_document['email']
	user_name = user_document['name']
	pic_link = user_document['picture']
	link = user_document['link']
#if user is not logging in for the first time during the session, get data of previous search history
	if user_email in cache:
		dict = cache[user_email][0]
		last10 = cache[user_email][1]
	logged_in = 'Logout'
	return main()


@route('/logout', method='GET')
def logout():
	global logged_in
	global dict, user_email, last10
#before logging out, update search history values for user in cache to be displayed upon next login
	cache[user_email] = [dict, last10]
	logged_in = 'Login'
	user_email = ''
	dict = {}
	last10 = []
	redirect(HOME_LINK)
	return main()


@route('/search', method='GET')
def search():
    global logged_in
    global last10
    string = request.query['keywords']
    string = re.sub(r'[^\w\s]','',string)   #filter punctuation
    l = string.lower().split()              #split by whitespaces
    cur = OrderedDict()
    updateHistory(l,cur)
    if logged_in == 'Logout':
    	updateHistory(l,dict)
	updateLast10(l,last10)
    
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
	<h3>Welcome, $user_name</h3>
	<img src = $pic_link alt = "profilepic" style = "width:100px;height:auto"/>	
	<br>
	<form action = "/logout" method = "get">
        <input id = "signin" type = "submit" value = "Sign Out">
        </form>
	</div>
	'''
    sign_out = Template(sign_out).safe_substitute(user_name = user_name, pic_link = pic_link)

#if search term contains more than one word, display results table
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

def updateLast10(l, last10):
#inputs: list l containing search terms, list last10 that will hold most recent search terms: the last term in the list being the most recent
	for i in l:
		if i in last10:
			last10.remove(i)
			last10.append(i)
		else:
			print l
			print last10
			last10.append(i)

run(host='0.0.0.0',port=80, debug=True)
#run localhost
#run(host='localhost', port=8080, debug=True)
