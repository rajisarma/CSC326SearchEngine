from bottle import *
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
#MAIN = "http://localhost:8080/redirect"
#for AWS instance
MAIN = "http://0.0.0.0:80/redirect"

#for localhost:
#HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080"
HOME_LINK = "https://accounts.google.com/logout?continue=https://appengine.google.com/_ah/logout?continue=http://ec2-34-196-113-147.compute-1.amazonaws.com"


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
final = []
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
    global logged_in, keywords, max_pages, current_page, final
    string = request.query['keywords']
    l = string.split()
    keywords = '+'.join(l)

    string = re.sub(r'[^\w\s]','',string)   #filter punctuation
    l = string.lower().split()              #split by whitespaces

#search by first word in database
    word = l[0]

#connect to database previously created using crawler
    db = sql.connect("SearchEngine.db")
    cursor = db.cursor()

#get word_id of search word
    cursor.execute("select word_id from Lexicon where word = (?)", (word,))
    word_id = cursor.fetchone()
    if word_id:
    	word_id = word_id[0]
    else:
	return error404("error")

#get doc_ids corresponding to word_id
    cursor.execute("select doc_ids from InvertedIndex where word_id = (?)", (word_id,))
    doc_ids = cursor.fetchone()[0]

#doc_ids is a string of numbers
#for each doc_id, check if page rank exists
    list_doc_ids = [int(e) for e in doc_ids.split()]
    page_rank_dict = {}
    for id in list_doc_ids:
    	cursor.execute("select doc_id, page_rank from PageRank where doc_id = (?)", (id,))
    	rank_result = cursor.fetchone()
	if rank_result:
		page_rank_dict[rank_result[0]] = rank_result[1]

#get urls for doc_ids having page rank
    url_dict = {}
    for key in page_rank_dict:
    	cursor.execute("select url from DocIndex where doc_id = (?)", (key,))
    	url_result = cursor.fetchone()
	url_dict[url_result[0]] = page_rank_dict[key]
    db.close()

#store urls in descending order of page rank in a list
#clear list of any previous searches
    final = []
    for l in sorted(url_dict,key=url_dict.get,reverse=True):
    	final.append(l)


#find number of pages needed to display all results
    max_pages = len(final)/5
    if len(final)%5 > 0:
    	max_pages += 1
#start at page 1
    current_page = 1
#show navigation for pages
    result = paginate_results(keywords)
    return print_page(keywords,1)


def paginate_results(keywords):
#displays navigation bar with page numbers to click through pages of results
	global current_page, final
	count = 0
	layout = ['''
	<style>
	.pagination a {
	color: black;
	padding: 8px 16px;
	text-decoration: none;
	}
	.pagination a.active {
	background-color: #9ACD32;
	color = white;
	border-radius: 3px;
	}
	.pagination a:hover:not(.active) {
	background-color: #ddd;
	border-radius: 3px;
	}
	</style>
	<nav> <div class = "pagination">
	<center>
	''']
#left arrow for previous page if not displaying the first page
	if current_page > 1:
		layout.append('<b><a href = "keywords=%s&page_no=%d"> &laquo; </a></b>' %(keywords, (current_page-1)))
#page numbers
	for p in range(max_pages):
		if current_page == p+1:
			layout.append('<b><a class = "active" href = "/keywords=%s&page_no=%d"> %d </a></b>' %(keywords,p+1,p+1))
		else:
			layout.append('<b><a href = "/keywords=%s&page_no=%d"> %d </a></b>' %(keywords,p+1,p+1))
			
#right arrow for next page if not displaying the last page
	if current_page <= max_pages-1:
		layout.append('<b><a href = "keywords=%s&page_no=%d"> &raquo; </a></b>' %(keywords, (current_page+1)))
	layout.append('<br></nav></div>')

	return '\n'.join(layout)

@route('/keywords=<keywords>&page_no=<page:int>', method = 'GET')
def print_page(keywords, page):
	global current_page
	current_page = page
	return result_template(final[5*page-5:5*page])

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
    urls = ['<br><br><div style = "display: inline-block; text-align: left;"><ul style="list-style-type:none">']
    for i in list:
        urls.append('<li> <a href = "%s"> %s </a> </li><br>' %(i,i))
    urls.append('</ul></div>')
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
def error404(error):
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

run(host='0.0.0.0',port=80, debug=True)
#run localhost
#run(host='localhost', port=8080, debug=True)
