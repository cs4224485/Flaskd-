# Author: harry.cai
# DATE: 2018/9/3


import redis

pool = redis.ConnectionPool(host='192.168.0.108', port=6379, password='123456')

r = redis.Redis(connection_pool=pool)
r.set('foo', 'Bar')

print(r.get('foo'))