
 
import nmap
from pprint import pprint

while True:
    print("""\nWhat do you want to do?\n
                1 - Get detailed info about a device
                2 - Scan IP for open ports with stealth scan
                e - Exit the application""")

    user_input = input("\nEnter your option: ")
    print()
    ip = input("\nPlease enter the IP address to scan: ")

    if user_input == "1":
        mynmap = nmap.PortScanner()


        print("\nThis may take a couple of minutes...\n")

        scan = mynmap.scan(ip, '1-1024', '-v -sS -sV ')

     
        print("\n= = = = = = = HOST {} = = = = = = =".format(ip))

        print("\n\nGENERAL INFO")

        try:
            mac = scan['scan'][ip]['addresses']['mac']
            print("\n-> MAC address: {}".format(mac))
        except KeyError:
            pass

        nm = nmap.PortScanner()
        scanner = nm.scan(ip, arguments='-O')
        if len(scanner['scan']) == 0:
            print("Host seems down. If it is really up, but blocking our ping probes")
        else:
            try:
                os = scan['scan'][ip]['osmatch'][0]['name']
                print("-> Operating system: {}".format(os))

            except:
                print("No OS detected")
           
            print("\n\nPORTS\n")

            for port in list(scan['scan'][ip]['tcp'].items()):
                print("-> {} | {} | {}".format(port[0], port[1]['name'], port[1]['state']))

            print("\n\nOTHER INFO\n")

            print("-> NMAP command: {}".format(scan['nmap']['command_line']))

    
        continue

    elif user_input == "2":
        mynmap = nmap.PortScanner()
        print('='*100)
        print('='*100)
        print("\nThis may take a couple of minutes...\n")

        scan = mynmap.scan(ip,ports = '1-1024', arguments = '-sS')
        if len(scan['scan']) == 0:
            print("Host seems down. If it is really up, but blocking our ping probes")

        for device in scan['scan']:
            mac_addr = scan['scan'][device]['addresses']['mac']
            print("Scanning IP: {} with MAC address: {}".format(scan['scan'][device]['addresses']['ipv4'],mac_addr))

            
            if 'tcp' in scan['scan'][device]:
                print("\nPorts open on {}:".format(device))
                for port in scan['scan'][device]['tcp'].items():
                    if port[1]['state'] == 'open':
                        print("-->" + str(port[0]) + "|" + port[1]['name'])
            else:
                print("\nNo open ports on {}:".format(device))

            if 'vendor' in scan['scan'][device]:
                print("The vendor is {}".format(scan['scan'][device]['vendor'][mac_addr]))
            else:
                pass
            if 'status' in scan['scan'][device]:
                status = scan['scan'][device]['status']['state']
                reason = scan['scan'][device]['status']['reason']
                print("Status: {} Reason: {}".format(status,reason)) 
            else:
                pass
        print('='*100)
        print('='*100)


        continue

    elif user_input == "e":
        print('\nExiting program...\n')

        break

    else:
        print("\nInvalid input. Try again!\n")

        continue

