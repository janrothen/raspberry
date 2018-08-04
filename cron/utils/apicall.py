import requests, json

def perform_request(method, url, json_data=None):
	data = None
	if json_data:
		data = json.dumps(json_data)

	#import pdb; pdb.set_trace()
	#msg = '{} {}'.format(method, url)
	#print(msg)

	r = None
	if method == 'GET':
		r = requests.get(url)
	elif method == 'DELETE':
		r = requests.delete(url)
	elif method == 'POST':
		r = requests.post(url, data=data)
	elif method == 'PUT':
		r = requests.put(url, data=data)

	result = r.text
	if not (r.status_code == 200 or r.status_code == 201):
		msg = '\nCode:   {}\nMsg:    {}\nRecord: {}'.format(r.status_code, result, data)
		raise ConnectionError(msg)

	return result
