Running Backend:



Frontend:
Public IP Address of live web server: 34.196.113.147
(http://ec2-34-196-113-147.compute-1.amazonaws.com/)
To access the frontend, go to the above link.
Type in a search word/term in the query box. A list of urls is returned if the search term exists in the database attached: SearchEngine.db
If search term does not exist (Eg. "cat") user is directed to a custom error page with a "page does not exist" message and link to go back to the home page of the website.

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


