import requests
import time
import platform
from requests.exceptions import ConnectionError

# Cheng Yi's recommendation
import os

def ping_test(url:str):
	print(f'Attempting to ping to {url} ')
	try:
	# ping uses ICMP protocol
	# pinging with 5 packets via -c flag with 10 second timeout
		if platform.system()=="Linux":
			response = os.popen(f'ping -c 5 -w 10 {url}')
		elif platform.system()=="Windows":
			response = os.popen(f'ping -n 5 -w 10000 {url}')
		elif platform.system()=="Darwin":
			os.popen(f"ping -c 5 -t 10 {url}")
		else:
			print("Cannot determine OS")
		for line in response.readlines():
			print(line)

	except:
		print(f"Failed with unparsed reason.")
    

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
		ping_test("google.com")
		return False
	except:
		print(f'Failed with unparsed reason.')
		return False


# --------------------------------------------------------------
### Charis's suggestion: Could use an existing library (eg. speedtest/pyspeedtest) for more accurate and comprehensive download speed measurement (streamline)
# Need to install speedtest module first (pip install speedtest-cli)
import speedtest

#creates an instance of the Speedtest class
#interact with the speedtest module and perform measurements
st = speedtest.Speedtest()
#retrieves information about available speedtest servers 
#chooses the one that is considered to be the "best" for the current location based on factors like ping and latency
best_server = st.get_best_server()

print(f"Testing download speed from server {best_server['host']}...")
#initiates a download test from the chosen server and measures the download speed
#bytes per second
download_speed = st.download()

#divides download speed in bytes per second by 1024**2 to convert it to megabits per second (Mbps)
# 1 byte = 8 bits - not sure if need to divide by 8 as well
# 1 kilobyte = 1024 bytes
# 1 megabit = 1024 bits
print(f"Download Speed: {download_speed / (1024**2):.2f} Mbps")
# --------------------------------------------------------------


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
		#time.sleep(2)
	print(f'Your download speed is {round(sum(all_speed)/len(all_speed))} Mbps')

def find_best_server(server):
	response_time = []
	for db in server:
		response = requests.get(db)
		response_time.append(response.elapsed.total_seconds())
	return server[response_time.index(min(response_time))]


database_server = ['http://link.testfile.org', 'http://www.speedtest.com.sg', 'http://ipv4.download.thinkbroadband.com']
database_url = {database_server[0]:['https://link.testfile.org/150MB', 'https://link.testfile.org/PDF200MB','https://link.testfile.org/70MB', 'https://link.testfile.org/PDF50MB'],
								database_server[1]:['http://www.speedtest.com.sg/test_random_100mb.zip?p=f08a4ffb20b7ca9a6ae12278aaed7fc617023819786578499a39e8a', 'http://www.speedtest.com.sg/test_random_100mb.zip']
								#'http://www.speedtest.com.sg/test_random_10mb.zip', 'http://www.speedtest.com.sg/test_random_10mb.zip?p=db5398b807ede45b8e05158294ce423a1702389203657865d3dda48'],
								,database_server[2]:['http://ipv4.download.thinkbroadband.com/100MB.zip','http://ipv4.download.thinkbroadband.com/200MB.zip', 'http://ipv4.download.thinkbroadband.com/50MB.zip']}



if (internet_connection_test()):
	user_select = int(input(f'''
Please select a number:
					1. Single file from a server
					2. Multiple files from same server
					3. Multiple files from different servers
					'''))
	### simple speed test ###
	if user_select == 1:
		single_test = []
		single_test.append(database_url[find_best_server(database_server)][0])
		run_speed_test(single_test)

	### multiple speed test single server ###
	elif user_select == 2:
		run_speed_test(database_url[find_best_server(database_server)])

	### multiple speed test multiple server ###
	elif user_select == 3:
		url_list = []
		for db in database_server:
			url_list.append(database_url[db][0])
		run_speed_test(url_list)

	else:
		print("Incorrect input... Please try again")
	

