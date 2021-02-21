import sys, argparse, socket, multiprocessing, subprocess, time
from datetime import datetime
from colorama import Fore, Back, Style 
import optparse

def banner():
   


    text = f""" {Fore.YELLOW}

  █████████  ███████████  ███████████
 ███░░░░░███░░███░░░░░███░█░░░███░░░█
░███    ░░░  ░███    ░███░   ░███  ░ 
░░█████████  ░██████████     ░███       
 ░░░░░░░░███ ░███░░░░░███    ░███    
 ███    ░███ ░███    ░███    ░███    
░░█████████  ███████████     █████   
 ░░░░░░░░░  ░░░░░░░░░░░     ░░░░░    
{Style.RESET_ALL}                                      """


    print(text)

def scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        res = s.connect_ex((ip, port))
        if res == 0:
            if port == 80:
                rsp = "HEAD / HTTP/1.1\r\nhost: "+ ip + "\r\n\r\n"
                s.send(rsp.encode())
            banner = s.recv(4096)
            msg = f"{Fore.GREEN}[+] Port  { str(port)}   open{Style.RESET_ALL}\n"
            msg += "------------------------\n" + f"{Fore.BLUE} {banner.strip().decode()} {Style.RESET_ALL}"
            print(msg + "\n------------------------\n")
        s.close()
    except socket.timeout:
        banner = "No Banner Message"
        if port == 53:
            banner = subprocess.getoutput("nslookup -type=any -class=chaos version.bind " + ip)
        msg = "[+] Port " + str(port) + " open\n"
        msg += "------------------------\n" + banner.strip()
        print(msg + "\n------------------------\n")
        s.close()

def main(target,startPort,endPort):
    try:
        start = datetime.now()
        print (f"{Fore.YELLOW}=================================================={Style.RESET_ALL}")
        print (f"{Fore.YELLOW}Scanning  {str(target)}  Ports:   {str(startPort)}  -   {str(endPort)}")
        print (f"{Fore.YELLOW}=================================================={Style.RESET_ALL}\n")
        ports = range(startPort, endPort+1)
        for port in ports:
            p = multiprocessing.Process(target=scan, args=(target,port,))
            p.start()
            time.sleep(0.1)
        # time.sleep(0.5)
        stop = datetime.now()
        print (f"{Fore.YELLOW}=================================================={Style.RESET_ALL}")
        print (f"{Fore.YELLOW}Scan Duration: {str(stop - start)} {Style.RESET_ALL}")
        print (f"{Fore.YELLOW}=================================================={Style.RESET_ALL}")
    except Exception as err:
        print(str(err))



help_text = f"""{Fore.RED}sudo Python3 scanner.py -t [ Domain Name ] or [IP] -s [Port range Begin] -e [Port range End]{Style.RESET_ALL}"""
parser = optparse.OptionParser(usage=help_text)
parser.add_option("-t", "--target", dest="target", help=f"{Fore.GREEN}Target ip or Domain Name{Style.RESET_ALL} ",  type=str)
parser.add_option("-s", "--startPort", dest="startPort", help=f"{Fore.GREEN}Start of port range{Style.RESET_ALL}",  type=int)
parser.add_option("-e", "--endPort", dest="endPort", help=f"{Fore.GREEN}End of the port range{Style.RESET_ALL}",  type=int)


banner()
if len(sys.argv[1:])==0:
    parser.print_help()
    parser.exit()

(options, arguments) = parser.parse_args()


main(options.target,options.startPort,options.endPort)
