# Request Parser
Simple Python Script for testing uptime.
Prints statistics on each request and evaluates if 200.
If request returns non 200, break script.
Written using Pycurl which is not ideal but only way I know to get fine-grain statistics in Python.

This project runs in conjunction with SpringBootSample which has a simple timestamp API that this script is meant to query.

### Run Locally
```bash
$ python3 genreq.py localhost:8080/timestamp
```

### Purpose
The purpose of these tools is to test blue-green deployment and whether or not a system is zero downtime.