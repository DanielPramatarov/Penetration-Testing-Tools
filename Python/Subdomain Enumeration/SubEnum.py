import requests 
import sys 

sub_list = open("subdomains.txt").read() 
subdoms = sub_list.splitlines()

for sub in subdoms:
    sub_domains = f"http://{sub}.test.com" 

    try:
        requests.get(sub_domains)
    
    except requests.ConnectionError: 
        print(f"{sub} is not valid sub domain")
    
    else:
        print("Valid domain: ",sub_domains)   
