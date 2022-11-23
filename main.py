import time
import os
import threading
import requests
from subprocess import check_output

#this command should rune in another thread
#os.system('amass enum -d orkhan-alibayli.com > /home/orkhan/python_amass.txt')

#this function will execute given system commands in another thred
def execute_amass():
	print("-- T1: this print function was called by another thread")
	os.system('amass enum -df /home/orkhan/automation/subdomains.txt >> /home/orkhan/automation/outputs/python_amass.txt')
	print('-- T1: execution of given command ended')


def execute_subjack():

	while(True):
		if(os.path.exists('/home/orkhan/automation/outputs/python_amass.txt')):
			print('-- T2: subjack is starting')
			os.system('subjack -w /home/orkhan/automation/outputs/python_amass.txt >> /home/orkhan/automation/outputs/python_subjack.txt')
			print('-- T2: subjack stopped')
			print('-- T2: subjack going to sleep for 10 seconds')
			time.sleep(10)
		else:
			print('-- T2: file does not exists yet. going to sleep for 10 seconds')
			time.sleep(10)


def sent_alert(line):
	sended_lines = []
	headers = {'Content-type: application/json'}
	url = 'https://hooks.slack.com/services/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'
	data = {"text":line}
	if(line not in sended_lines):
		response = requests.post(url, json = data)
		sended_lines.append(line)
	else:
		print('-- sent_alert: this line is already sent')


def normalize_line(line):
	chars = '[]'
	print(line)
	for char in chars:
		line = line.replace(char, '')
	line = 'This service is vulnerable to subdomain takeover: ' + line + ''
	#print(f'|{line}|')
	return line


def read_subjack_file():

	vulnerable_services = ['HEROKU','INTERCOM','JETBRAINS','PANTHEON','README','S3 BUCKET','SHOPIFY','SIMPLEBOOKLET','SMUGMUG','SURGE','TEAMWORK','TICTAIL','TUMBLR','USERVOICE','VEND','WEBFLOW','WISHPOND','WORDPRESS','WORKSITES.NET','ZENDESK']

	while(True):
		if(os.path.exists('/home/orkhan/automation/outputs/python_subjack.txt')):
			with open('/home/orkhan/automation/outputs/python_subjack.txt', 'r') as f:
				while(True):
					line = f.readline()
					
					if not line:
						#offset= f.tell()
						print('-- T3: new line not found. Going to sleep for 10 seconds')
						time.sleep(10)
					else:
						for service in vulnerable_services:
							if service in line:
								print('-- T3: VULNERABLE SUBDOMAIN FOUND')
								#os.system('whoami')
								line = normalize_line(line)
								sent_alert(line)
		else:
			print('-- T3: python_subjack file does not exists yet')
			print('-- T3: going to sleep for 10 seconds')
			time.sleep(10)


def main():
	# waiting for amass execution
	while(True):
		pid_of_amass = None
		pid_of_subjack = None
		try:
			pid_of_amass = check_output(['pidof', 'amass'])
			pid_of_subjack = check_output(['pidof', 'subjack'])
		except:
			print('-- T0: an exception occured. probably process with given name does not exists')
		
		if(pid_of_amass == None):
			print('-- T0: execution of amass finished')
		else:
			print('-- T0: pid of amass is ', pid_of_amass)

		if(pid_of_subjack == None):
			print('-- T0: execution of subjack finished')
		else:
			print('-- T0: pid of subjack ', pid_of_subjack)




		time.sleep(10)


if __name__ == '__main__':

	#first thred for executing system commands
	t_amass = threading.Thread(target = execute_amass)
	t_amass.start()

	t_subjack = threading.Thread(target = execute_subjack)
	t_subjack.start()

	t_read = threading.Thread(target = read_subjack_file)
	t_read.start()

	main()


