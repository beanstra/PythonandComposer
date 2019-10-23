import time

import redis
from flask import Flask
from flask import request
from flask import jsonify
import socket

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    # hostname = socket.gethostbyname()
    # IPAddr = socket.gethostbyname(hostname)
    # ip_address = socket.gethostbyaddr(socket.gethostbyname()) 
    # IPaddr = socket.gethostbyaddr(ip_address)
    ip_address = request.remote_addr
    return 'Hello World. Sjoerd & Jako here ! this app has been seen {} times.\n'.format(count) + 'You are browsing from:' + ip_address