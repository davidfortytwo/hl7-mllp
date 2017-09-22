# hl7-mllpFuzzer

hl7-mllpFuzzer can be used to determine which message types are accepted by a TCP-Listener. The most common message types are included.

**Please don't use hl7-mllpFuzzer in a productive environment, you may seriously harm people. This is for testing purpose only.**

Usage:
```
root@kali:~# python hl7_fuzz.py -h
usage: hl7_fuzz.py [-h] [-f FILENAME] host port level

positional arguments:
  host                  host to connect to
  port                  port to connect to
  level                 "low", "high", "custom" for hl7 file input

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        path to hl7 file
```

Example:
```
root@kali:~# python hl7_fuzz.py 192.168.188.185 6661 low
[+] Start level low
[+] Message type accepted: ADT = Admit Discharge Transfer
[+] Finished sending 12 messages.
```
