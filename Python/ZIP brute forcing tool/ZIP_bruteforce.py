
import zipfile
import os
from colorama import Fore, Back, Style 


count = 1
file_name = "Extracted files from ZIP"
wordlistPath = str(input(f"{Fore.YELLOW}Enter Wordlist path:{Style.RESET_ALL} "))
ZIPpath = str(input(f"{Fore.YELLOW}Enter ZIP file path:{Style.RESET_ALL} "))


with open(wordlistPath,'rb') as text:
    for entry in text.readlines():
        password = entry.strip()
        try:
            with zipfile.ZipFile(ZIPpath,'r') as zf:
                path = os.getcwd() + "/Python/ZIP brute forcing tool"+"/" + file_name

                zf.extractall(path,pwd=password)

                data = zf.namelist()[0]

                data_size = zf.getinfo(data).file_size

                print(f"[+]******************************\n{Fore.GREEN}[+] Password found!{Style.RESET_ALL} ~ {password.decode('utf8')}\n ~{data}\n ~{data_size}\n******************************")
                print (f"Files are stored in this directory => {Fore.BLUE}{path}{Style.RESET_ALL}")

                break

        except:
            number = count
            print(f"[{number}] {Fore.RED}[-] Password failed!{Style.RESET_ALL} - {password.decode('utf-8')}" )
            count += 1
            pass


