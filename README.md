# Subdomain takeover enumeration script

This script executes three different threads for three different aims:
1. Subdomain enumeration
2. Checking for potentially vulnerable subdomains
3. Sending potentially vulnerable domains to the researcher via an alert

The first task is accomplished by using OWASP Amass ( https://github.com/OWASP/Amass ). The script continuously checks for the PID of Amass process. At the moment the checking of PID does not affect the general purpose of the script. But I wrote this for potential future features which will be able to use this PID.

In the second task subjack tool ( https://github.com/haccer/subjack ) helps to solve the problem of verifying vulnerabilities.

I used the requests module for solving this problem. There is one thread in the program which continues reading the output of subjack and if there is a new line in the file program will send me a slack notification.


For more information about subdomain takeover vulnerabilities refer to my blog post in medium: https://medium.com/@orkhan_alibayli/subdomain-takeover-95646de1f436
