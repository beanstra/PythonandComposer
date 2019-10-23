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

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
    print(request.remote_addr)

if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    print(request.environ['REMOTE_ADDR'])
else:
    print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World. Sjoerd & Jako here ! this app has been seen {} times.\n'.format(count)