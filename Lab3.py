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
import sqlite3 as sql

#for localhost
MAIN = "http://localhost:8080/redirect"
#for AWS instance
#MAIN = "http://0.0.0.0:80/redirect"

#for localhost:
HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080"
#HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://0.0.0.0:80"


#from json file, get values needed to start login process
with open("client_secrets.json") as json_file:
	client_secrets = json.load(json_file)
	CLIENT_ID = client_secrets["web"]["client_id"]
	CLIENT_SECRET = client_secrets["web"]["client_secret"]
	SCOPE = client_secrets["web"]["auth_uri"]
	REDIRECT_URI = client_secrets["web"]["redirect_uris"][0]
	GOOGLE_SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

keywords = ''
logged_in = 'Login'
user_email = ''
user_name = ''
pic_link = ''
test = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11', 'test12']
current_page = 1
max_pages = 0


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

    if logged_in == 'Logout':
        return sign_out, f
    else:
        return sign_in, f


@route('/login', 'GET')

def login():
	global logged_in
	if logged_in == "Login":
		flow = flow_from_clientsecrets("client_secrets.json",scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri = REDIRECT_URI)
		uri = flow.step1_get_authorize_url()
		redirect(str(uri))
	else:
		logout()


@route('/redirect')
def redirect_page():
	global logged_in
	global user_email, user_name, pic_link, link
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
	user_name = user_document['name']
	pic_link = user_document['picture']
	link = user_document['link']
#if user is not logging in for the first time during the session, get data of previous search history
	#if user_email in cache:
	#	dict = cache[user_email][0]
	#	last10 = cache[user_email][1]
	logged_in = 'Logout'
	return main()


@route('/logout', method='GET')
def logout():
	global logged_in
	#global dict, user_email, last10
#before logging out, update search history values for user in cache to be displayed upon next login
	#cache[user_email] = [dict, last10]
	logged_in = 'Login'
	user_email = ''
	#dict = {}
	#last10 = []
	redirect(HOME_LINK)
	return main()


@route('/search', method='GET')
def search():
    global logged_in, keywords, test, max_pages, current_page
    string = request.query['keywords']
    l = string.split()
    keywords = '+'.join(l)

    string = re.sub(r'[^\w\s]','',string)   #filter punctuation
    l = string.lower().split()              #split by whitespaces
    
    word = l[0]
    #conn = sql.connect('test.db')

    #cursor = conn.cursor()
    #cursor.execute("select doc_ids from lexicon inner join inverted_index on lexicon.word_id = inverted_index.word_id")





#if results found: else: call error handler:
#list containing urls to be printed
    max_pages = len(test)/5
    if len(test)%5 > 0:
    	max_pages += 1
    current_page = 1
    result = paginate_results(keywords)
    return print_page(keywords,1)

def paginate_results(keywords):
	global test
	count = 0
	layout = ['''
	<style>
	.pagination a {
	color: black;
	padding: 8px 16px;
	text-decoration: none;
	}
	.pagination a.active {
	background-color: #0000FF;
	color = white;
	border-radius: 5px;
	}
	.pagination a:hover:not(.active) {
	background-color: #ddd;
	border-radius: 5px;
	}
	</style>
	<nav> <div class = "pagination">
	<center>
	''']
	for p in range(max_pages):
		layout.append('<a href = "/keywords=%s&page_no=%d"> %d </a>' %(keywords,p+1,p+1))
	layout.append('<br></nav></div>')

	return '\n'.join(layout)

@route('/keywords=<keywords>&page_no=<page:int>', method = 'GET')
def print_page(keywords, page):
	current_page = page
	return result_template(test[5*page-5:5*page])

def result_template(list):
    global keywords
    f ='''
        <br>
        <style>
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
    back = '<br><center><form action = "/"> <input id = "button" type = "submit" value = "Home"> </form></center>'
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
    result = paginate_results(keywords)
    urls = ['<ul>']
    for i in list:
        urls.append('<li> %s </li>' %i)
    urls.append('</ul>')
    string = '''
		<style>
	        #signin {
	        width: 150px;
		font-size: 20px;
		}
		</style>
		<center>
		<br><br>
		<style>
		#button {
		width: 70px;
		font-size: 20px;
		}
		</style>
		<body bgcolor = "#F0B27A"/></center>'''
    if logged_in == "Logout":
        return sign_out, string, f, back, result, '\n'.join(urls)
    else:
	return sign_in, string, f, back, result, '\n'.join(urls)


@error(404)
def error_404():
    back = '<br><br><center><form action = "/"> <input id = "button" type = "submit" value = "Home"> </form></center>'
    string = '''
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
		<body bgcolor = "#F0B27A"> This page does not exist </body></center>'''
    return string, back

#run(host='0.0.0.0',port=80, debug=True)
#run localhost
run(host='localhost', port=8080, debug=True)
