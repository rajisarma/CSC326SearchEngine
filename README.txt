Files to be reviewed:
Front end: 
Lab3.py
Backend:
run_backend_test.py
crawler.py
pageRank.py
urls.txt

The following is the documentation of the frontend, backend and benchmarking results

Backend:

run_backend_test.py
To demonstrate crawler's functionality a single Python script run_backend_test.py has been created.
To run run_backend_test.py:
Step1: Install BeautifulSoup and bottle using the following commands in terminal (if not already installed) using the command:
	1) cd into the directory of the BeautifulSoup and bottle library
	2) type the command:  python setup.py install --user
Step 2: cd into directory containing the run_backend_test.py, crawler.py, pageRank.py and urls.txt
Step 3: run the command python run_backend_test.py
Step 4: Observe the output which prints the page rank score of the documents returned from the page rank algorithm (in pageRank.py) invoked from crawler object (refer to crawler.py) in a readable "pretty" format

Example:
urls/documents in urls.txt which is used in run_backend_test.py are:
http://sdraper.ece.wisc.edu/
https://www.nal.utoronto.ca/

Expected output(truncated):

ug74:~/Desktop/csc326/lab1_group_37% python run_backend_test.py
deleting any exisiting tables
creating databases
in crawl
2
document title=u'Alberto Leon-Garcia'
    num words=283
    url='https://www.nal.utoronto.ca/'
document title=u'Alberto Leon-Garcia - Teaching'
    num words=436
    url=u'https://www.nal.utoronto.ca/teaching.html'
document title=u'Alberto Leon-Garcia - Students'
    num words=1765
    url=u'https://www.nal.utoronto.ca/students.html'
document title=u'Alberto Leon-Garcia - Presentations'
    num words=238
    url=u'https://www.nal.utoronto.ca/presentations.html'
document title=u'Alberto Leon-Garcia - Patents'
    num words=212
    url=u'https://www.nal.utoronto.ca/patents.html'
document title=u'Dr Alberto Leon-Garcia - Recent Publications'
    num words=1895
    url=u'https://www.nal.utoronto.ca/recentpublications.html'
document title=u'Alberto Leon-Garcia - Books'
    num words=226
    url=u'https://www.nal.utoronto.ca/books.html'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#VANI_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#ASA_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#OptFabforDataCtrs_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#SmartGrids_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#GrnNtwrk_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#NtwrkCriticality_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#CVST_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html#SAVI_Res'
document title=u'Alberto Leon-Garcia - Research'
    num words=992
    url=u'https://www.nal.utoronto.ca/research.html'
document title=u'Alberto Leon-Garcia - Awards'
    num words=140
    url=u'https://www.nal.utoronto.ca/awards.html'
document title=u'Alberto Leon-Garcia - Profile'
    num words=287
    url=u'https://www.nal.utoronto.ca/profile.html'
document title=u'Alberto Leon-Garcia'
    num words=283
    url=u'https://www.nal.utoronto.ca/index.html'
<urlopen error [Errno -2] Name or service not known>
document title=u'University of Toronto'
    num words=618
    url=u'http://www.utoronto.ca/'
document title=u"Stark Draper's Webpage"
    num words=39
    url='http://sdraper.ece.wisc.edu/'
    num words=10
    url=u'http://sdraper.ece.wisc.edu/backgroundDir/frame.html'
    num words=10
    url=u'http://sdraper.ece.wisc.edu/groupDir/frame.html'
    num words=10
    url=u'http://sdraper.ece.wisc.edu/teachingDir/frame.html'
    num words=10
    url=u'http://sdraper.ece.wisc.edu/researchDir/frame.html'
Document ID - Page Range Score results
Presented in the order of greatest to least page rank scored document or url
[(2, 0.014550813863295257),
 (4, 0.014434132807989709),
 (5, 0.014434132804667566),
 (6, 0.014434132801647011),
 (7, 0.014434132798775832),
 (8, 0.01443413279741462),
 (9, 0.014434132796121078),
 (10, 0.014434132794891839),
 (11, 0.014434132793723714),
 (12, 0.01443413279261366),
 (13, 0.01443413279155879),
 (14, 0.014434132790556362),
 (15, 0.014434132789603767),
 (16, 0.01443413278869853),
 (17, 0.014434132787127667),
 (18, 0.014434132786285362),
 (19, 0.014434132784872123),
 (20, 0.014434132783648627),
 (21, 0.014434132783092413),
 (1, 0.007416962270235409),
 (106, 0.0071428571428571435)]


To run 
In general:
Crawler.py:
To run crawler.py:
Step 1: cd into the directory containing crawler.py and urls.txt
Step 2: In terminal, run python crawler.py


Frontend:
Public IP Address of live web server: 34.196.113.147
(http://ec2-34-196-113-147.compute-1.amazonaws.com/)
To access the frontend, go to the above link.
Type in a search word/term in the query box. A list of urls is returned if the search term exists in the database attached: SearchEngine.db
If search term does not exist (Eg. "cat") user is directed to a custom error page with a "page does not exist" message and link to go back to the home page of the website.

Note: Google Login is still available but the behaviour is the SAME when logged in or in anonymous mode

Benchmarking:
A separate instance at 34.238.14.109 was created for benchmarking.
Benchmark Setup:
1. To install Apache: $ sudo apt-get install apache2-utils
2. To install sysstat: $ sudo apt-get install sysstat dstat
Following this, 
$ ab -n 1000 -c 50 http://34.238.14.109/?keywords=helloworld+foo+bar 
can be used to retrieve necessary data
Output is as follows:



Benchmarking output

Maximum number of connections that can be handled by the server before any
connection drops:
50 concurrent connections

Maximum number of requests per second (RPS) that can be sustained by the server
when operating with maximum number of connections:
Requests per second:	1156.19 [#/sec] (mean)

Average and 99 percentile of response time or latency per request:
Average: 			0.865 [ms] (mean, across all concurrent requests)
99th Percentile: 	50 [ms]


Utilization of CPU, memory, disk IO, and network when max performance is sustained:
CPU: 			20%
Memory:			0.5%
Disk IO:		0%
Network In:		14868954 Bytes
Network Out:	14157068 Bytes



Output from ubuntu terminal
ubuntu@ip-172-31-41-72:~/bm$ ab -n 1000 -c 50 http://34.238.14.109/?keywords=helloworld+foo+bar
This is ApacheBench, Version 2.3 <$Revision: 1528965 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 34.238.14.109 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Apache/2.4.7
Server Hostname:        34.238.14.109
Server Port:            80

Document Path:          /?keywords=helloworld+foo+bar
Document Length:        11510 bytes

Concurrency Level:      50
Time taken for tests:   0.865 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      11783000 bytes
HTML transferred:       11510000 bytes
Requests per second:    1156.19 [#/sec] (mean)
Time per request:       43.246 [ms] (mean)
Time per request:       0.865 [ms] (mean, across all concurrent requests)
Transfer rate:          13304.07 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.2      1       7
Processing:     6   41   6.2     42      51
Waiting:        2   41   6.2     41      50
Total:         10   42   5.3     43      51

Percentage of the requests served within a certain time (ms)
  50%     43
  66%     43
  75%     44
  80%     45
  90%     47
  95%     48
  98%     50
  99%     50
 100%     51 (longest request)
ubuntu@ip-172-31-41-72:~/bm$ 


