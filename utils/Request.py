import requests, json

from enum import Enum

class Method(Enum):
	GET = 1
	POST = 2
	PUT = 3
	DELETE = 4

class Request(object):
	def get(self, url):
		return self.perform(Method.GET, url)

	def post(self, url, json_data=None):
		return self.perform(Method.POST, url, json_data)

	def put(self, url, json_data=None):
		return self.perform(Method.PUT, url, json_data)

	def delete(self, url):
		return self.perform(Method.DELETE, url)

	def perform(self, method, url, json_data=None):
		data = None
		if json_data:
			data = json.dumps(json_data)

		#import pdb; pdb.set_trace()
		#msg = '{} {}'.format(method, url)
		#print(msg)

		r = None
		if method == Method.GET:
			r = requests.get(url)
		elif method == Method.POST:
			r = requests.post(url, data=data)
		elif method == Method.PUT:
			r = requests.put(url, data=data)
		elif method == Method.DELETE:
			r = requests.delete(url)

		result = r.text
		if not (r.status_code == 200 or r.status_code == 201):
			msg = '\nCode: {}\nResult: {}\nData: {}'.format(r.status_code, result, data)
			raise ConnectionError(msg)

		return result