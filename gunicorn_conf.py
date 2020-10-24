bind = "127.0.0.1:5001"
x_forwarded_for_header = "X-Real-IP"
access-logfile = "-"
access_logformat = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s"'