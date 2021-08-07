import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

NS = dr.Resolver()

Subdomains = []

def AXFR(domain, nameserver):

    try:
        axfr = dz.from_xfr(dq.xfr(nameserver, domain))

        if axfr:
            print('[*] Successful Zone Transfer from {}'.format(nameserver))

            for record in axfr:
                Subdomains.append('{}.{}'.format(record.to_text(), domain))

    except Exception as error:
        print(error)
        pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="dns-axfr.py", epilog="DNS Zonetransfer Script", usage="dns-axfr.py [options] -d <DOMAIN>", prefix_chars='-', add_help=True)

    parser.add_argument('-d', action='store', metavar='Domain', type=str, help='Target Domain.\tExample: inlanefreight.htb', required=True)
    parser.add_argument('-n', action='store', metavar='Nameserver', type=str, help='Nameservers separated by a comma.\tExample: ns1.inlanefreight.htb,ns2.inlanefreight.htb')
    parser.add_argument('-v', action='version', version='DNS-AXFR - v1.0', help='Prints the version of DNS-AXFR.py')

    args = parser.parse_args()

    Domain = args.d
    NS.nameservers = list(args.n.split(","))

    if not args.d:
        print('[!] You must specify target Domain.\n')
        print(parser.print_help())
        exit()

    if not args.n:
        print('[!] You must specify target nameservers.\n')
        print(parser.print_help())
        exit()

    
    for nameserver in NS.nameservers:

        AXFR(Domain, nameserver)

    if Subdomains is not None:
        print('-------- Found Subdomains:')

        for subdomain in Subdomains:
            print('{}'.format(subdomain))

    else:
        print('No subdomains found.')
        exit()
    print(len(Subdomains))