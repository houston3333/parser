import requests


proxies = open("proxies.txt", "r").read().strip().split("\n")


def get(url, proxy): 
	""" 
	Sends a GET request to the given url using given proxy server. 
	The proxy server is used without SSL, so the URL should be HTTP. 
 
	Args: 
		url - string: HTTP URL to send the GET request with proxy 
		proxy - string: proxy server in the form of {ip}:{port} to use while sending the request 
	Returns: 
		Response of the server if the request sent successfully. Returns `None` otherwise. 
 
	""" 
	try: 
		r = requests.get(url, proxies={"http": f"http://{proxy}"}) 
		if r.status_code < 400: # client-side and server-side error codes are above 400 
			return r 
		else: 
			print(r.status_code) 
	except Exception as e: 
		print(e) 
 
	return None


def check_proxy(proxy): 
	""" 
	Checks the proxy server by sending a GET request to httpbin. 
	Returns False if there is an error from the `get` function 
	""" 
 
	return get("http://httpbin.org/ip", proxy) is not None 
 
available_proxies = list(filter(check_proxy, proxies))

