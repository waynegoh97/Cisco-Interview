import requests
import time
from requests.exceptions import ConnectionError

def internet_connection_test():
	url = 'https://www.google.com/'
	print(f'Attempting to connect to {url} to determine internet connection status.')
	
	try:
		print(url)
		resp = requests.get(url, timeout = 10)
		resp.text
		resp.status_code
		print(f'Connection to {url} was successful.')
		return True
	except ConnectionError as e:
		requests.ConnectionError
		print(f'Failed to connect to {url}.')
		return False
	except:
		print(f'Failed with unparsed reason.')
		return False

def download_speed_test(url):
	start_time = time.time()
	response = requests.get(url, stream=True) #stream=True allow files to download response in stream of bytes
	overall_data = 0
	for data in response.iter_content(chunk_size=4096):
		overall_data += len(data) #data is byte object, len returns length in bytes
	end_time = time.time()
	total_time = end_time - start_time
	data_in_MB = overall_data / (1024*1024)
	speed_Mbps = (data_in_MB*8) / total_time
	return speed_Mbps

def run_speed_test(urls):
	all_speed = []
	print('Initialising speed test...')
	for url in urls:
		speed = download_speed_test(url)
		all_speed.append(speed)
		time.sleep(2)
	print(f'Your download speed is {round(sum(all_speed)/len(all_speed))} Mbps')
	
urls = [ 'http://link.testfile.org/150MB',
				 'http://www.speedtest.com.sg/test_random_100mb.zip?p=f08a4ffb20b7ca9a6ae12278aaed7fc617023819786578499a39e8a',
				 'https://link.testfile.org/PDF200MB']

internet_connection_test()
run_speed_test(urls)
