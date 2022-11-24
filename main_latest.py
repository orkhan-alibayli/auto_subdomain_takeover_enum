import time
import os
import threading
from subprocess import check_output
import requests

sended_urls = []  #caching sended urls in a list for not sending same url multiple times
vulnerable_services = ['AFTERSHIP','AHA','APIGEE','AZURE','BIGCARTEL','BITBUCKET','BRIGHTCOVE','CAMPAIGNMONITOR','GETRESPONSE','GITHUB','GHOST','HELPJUICE','HELPSCOUT','HEROKU','INTERCOM','JETBRAINS','PANTHEON','README','S3 BUCKET','SHOPIFY','SIMPLEBOOKLET','SMUGMUG','SURGE','TEAMWORK','TICTAIL','TUMBLR','USERVOICE','VEND','WEBFLOW','WISHPOND','WORDPRESS','WORKSITES.NET','ZENDESK']


def execute_amass():
    '''Executing subdomain enumeration tool OWASP Amass as shell command and writing results to a file'''

    print("-- T1: this print function was called by another thread")
    os.system('amass enum -d orkhan-alibayli.com >> /home/orkhan/automation/outputs/python_amass.txt')
    print('-- T1: execution of given command ended')


def execute_subjack():
    '''Executing subjack tool for detecting vulnerable subdomains and writing results to a file.
    Executing ends when programs ends. Untill that subjack reading file which written by Amass.
    '''

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


def sent_heart_beat():
    pass


def sent_alert(line_as_list):
    '''Using requests module sends https request to slack api for alerting.
    Gets vulnerable service and vulnerable url as a list. For example, ['GITHUB', 'subdomain.example.com']
    '''

    headers = {'Content-type: application/json'}
    url = 'https://hooks.slack.com/services/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'

    if(line_as_list[1] not in sended_urls):
        data = {"text":str(line_as_list)}
        response = requests.post(url, json = data)
        sended_urls.append(line_as_list[1])
    else:
        print('-- Function sent_alert: this line has already sent')


def normalize_line(line):
    '''Splits output of subjack which written to a file line by line and returns splitted parts as list'''

    line_as_list = line.split()
    return line_as_list


def read_subjack_file():
    '''For every 10 seconds cheks whether subjack has new output or not. If yes then call normalize_line() and sent_alert() functions respectively.'''

    while(True):
        if(os.path.exists('/home/orkhan/automation/outputs/python_subjack.txt')):
            with open('/home/orkhan/automation/outputs/python_subjack.txt', 'r') as f:
                while(True):
                    line = f.readline()
                    if not line:
                        print('-- T3: new line not found. Going to sleep for 10 seconds')
                        time.sleep(10)
                    else:
                        for service in vulnerable_services:
                            if service in line:
                                print('-- T3: VULNERABLE SUBDOMAIN FOUND')
                                line_as_list = normalize_line(line)
                                sent_alert(line_as_list)
        else:
            print('-- T3: python_subjack file does not exists yet')
            print('-- T3: going to sleep for 10 seconds')
            time.sleep(10)


def main():
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

