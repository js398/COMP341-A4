import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def is_prime(n):
	if n<=1: 
		return False
	elif n<=3:
		cache.lpush('primes',n)
		return True
	elif n%2==0 or n%3==0:
		return False
	i=5
	while(i*i<=n):
		if n%i==0 or n%(i+2)==0:
			return False
		i=i+6
	cache.lpush('primes',n)
	return True

@app.route('/isPrime/<int:n>')
def prime(n):
	status=is_prime(n)
	if status:
		return '{} is prime\n'.format(n)
	else:
		return '{} is not prime\n'.format(n)

@app.route('/primeStored')
def store_primes():
	return str(cache.lrange('primes',0,-1))+"\n"

