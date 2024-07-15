# WafflesBuster
### -> A simple Multi-threaded directory buster. 

I created this script to directory bust a website and when '429' code is returned pause the script. '429' was the code a website was giving out when it blocked my IP.
This way, I could change my IP address with a VPN, before unpausing the script.

### Running normally
![image](https://github.com/WafflesExploit/WafflesBuster/assets/15943431/104f0e66-53a4-4811-b67a-ff760932892b)
### When request returns specified pause code
![image](https://github.com/WafflesExploit/WafflesBuster/assets/15943431/131aa7c8-a25f-4e63-865a-40405e1dd5d3)

Usage:
```
usage: wafflesbuster.py [-h] [-u URL] [-w WORDLIST] [-p PAUSE] [-s [STATUS]] [-t [THREADS]] [-o [OUTPUT]] [-v]
                        [-c]

-> Directory Brute-forcer

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL.
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist containing the URLs to scan.
  -p PAUSE, --pause PAUSE
                        Pauses based on status. Default: 429
  -s [STATUS], --status [STATUS]
                        Specifies the Status code to match. Example:'200-299,301,302'
  -t [THREADS], --threads [THREADS]
                        Number of threads to use. Default: 5
  -o [OUTPUT], --output [OUTPUT]
                        Outputs results to a file.
  -v, --verify          Set to false if the website doesn't use SSL.
  -c, --color           Colorize output. Default=false
                                                       
```
