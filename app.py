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

import urllib
import re

def get_external_ip():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address

if __name__ == '__main__':
  print( get_external_ip() )

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World. Sjoerd & Jako here ! this app has been seen {} times.\n'.format(count)