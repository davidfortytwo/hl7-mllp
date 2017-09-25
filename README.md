# hl7-mllpFuzzer

hl7-mllpFuzzer can be used to determine which message types are accepted by a MLLP Server. The most common message types are included.

The "injection" mode can be used to test interfaces and following applications for different injection vulnerabilities.
hl7_fuzzer will build "Evil Messages" and send them to the MLLP Server.

Check out this site if you need more Message templates:
http://www.mieweb.com/wiki/Sample_HL7_Messages#MDM.5ET02

Don't have a test Environment yet? Use this tools:
http://smarthl7.com/

Special thanks to this great project:
https://python-hl7.readthedocs.io/en/latest/

**Please don't use hl7-mllpFuzzer in a productive environment, you may seriously harm people. This is for testing purpose only.**

Example usage fuzz mode with builtin mode:
```
root@kali:~# python hl7_fuzz.py 192.168.188.3 1234 fuzz -p high
[+] Start payload high
[+] Starting MLLP sender
[+] Message type accepted: ADT = Admit Discharge Transfer
...
[+] Finished sending 4 messages.
```


Example usage fuzz mode with hl7 file input:
```
root@kali:~# python hl7_fuzz.py 192.168.188.3 1234 fuzz -p custom -f /root/test.hl7
[+] Start payload custom
[+] Starting MLLP sender
[+] Message type accepted: ADT = Admit Discharge Transfer
[+] Finished sending /root/test.hl7.
```

Show help injection mode:
```
C:\Python27>python.exe hl7_inject.py -h
usage: hl7_inject.py [-h] [-p PAYLOAD] host port mode file inject
positional arguments: 
host                  host to connect to  
port                  port to connect to  
mode                  "MSSQL", "MYSQL", "custom", "file" 
file                  path to hl7 file 
inject                for example: "PID.5.1" = Firstname

optional arguments:  
-h, --help                        show this help message and exit  
-p PAYLOAD, --payload PAYLOAD     path to custom payload file
```

Example usage injection mode with builtin payload:
```
C:\Python27>python.exe hl7_inject.py 127.0.0.1 1234 MSSQL C:\Python27\ADT_20150614_080631_2216_A03.HL7 PID.5.1
[+] Starting injection
[+] 16 messages send.
```


Example usage injection mode with custom payload:
```
C:\Python27>ile input:```
root@kali:~# python hl7_fuzz.py 192.168.188.3 1234 fuzz -p custom -f /root/test.hl7
[+] Start payload custom
[+] Starting MLLP sender
[+] Message type accepted: ADT = Admit Discharge Transfer
[+] Finished sending /root/test.hl7.
```

Show help injection mode:
```
C:\Python27>python.exe hl7_inject.py -h
usage: hl7_inject.py [-h] [-p PAYLOAD] host port mode file inject
positional arguments: 
host                  host to connect to  
port                  port to connect to  
mode                  "MSSQL", "MYSQL", "custom", "file" 
file                  path to hl7 file 
inject                for example: "PID.5.1" = Firstname

optional arguments:  
-h, --help                        show this help message and exit  
-p PAYLOAD, --payload PAYLOAD     path to custom payload file
```

Example usage injection mode with builtin payload:
```
C:\Python27>python.exe hl7_inject.py 127.0.0.1 1234 MSSQL C:\Python27\ADT_20150614_080631_2216_A03.HL7 PID.5.1
[+] Starting injection
[+] 16 messages send.
```


Example usage injection mode with custom payload:
```
C:\Python27>python.exe hl7_inject.py 127.0.0.1 1234 custom C:\Python27\ADT_20150614_080631_2216_A03.HL7 PID.5.1
[+] Starting injection
Enter your payload: 'This is a really Evil String'
[+] Starting injection
[+] Message send.
...
```


Example usage injection mode with custom payload from file:
```
C:\Python27>python.exe hl7_inject.py 127.0.0.1 1234 file C:\Python27\ADT_20150614_080631_2216_A03.HL7 PID.5.1 -p C:\Python27\payload.txt[+] Starting injection[+] 
4 messages send.
```
