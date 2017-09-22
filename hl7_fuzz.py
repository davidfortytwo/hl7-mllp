import hl7
import datetime
import time
import sys
import os
import argparse

from hl7.client import MLLPClient

def adtSample():
	adtMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|||ADT^A01|MSG123|P|2.2||||AL|\r'
	adtMessage += 'PID|||P1||Lastname1^Firstname1^MiddleName1^^^Degree1|MotherMaidenName1|19720828|M|||Street 123^^New York^^12345||0049123456789||||||SSN1||||||||^Occupation1\r'
	adtMessage += 'PV1|1|O|Room 123|||||^Smith^John^^^^MD|||||||||||V1|20100607065608|||||||||||||||||||ServicingFacility1|||||20100608065608\r'
	adtMessage += 'IN1|1|111||Insurance\r'
	adtMessage += 'ZPI|V1Free1|V1Free2|V1Free3|V1Free4|V1Free5|V1Free6|V1Free7|V1Free8|V1Free9|V1Free10|V1Free11|V1Free12|V1Free13|V1Free14|V1Free15|||||History1|Diagnose1|'
	return adtMessage
	
def ormSample():
	ormMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|20100607065608||ORM^O01|MSG123|P|2.2||||AL|\r'
	ormMessage += 'PID|||P1||Lastname1^Firstname1^MiddleName1^^^Degree1|MotherMaidenName1|19720828|M|||Street 123^^New York^^12345||0049123456789||||||SSN1||||||||^Occupation1\r'
	ormMessage += 'PV1|1|O|Room 123|||||^Lastname2^Firstname2^^^^MD|||||||||||V1||||||||||||||||||||ServicingFacility1|||||20100608065608\r'
	ormMessage += 'IN1|1|111||Insurance\r'
	ormMessage += 'ZPI|V1Free1|V1Free2|V1Free3|V1Free4|V1Free5|V1Free6|V1Free7|V1Free8|V1Free9|V1Free10|V1Free11|V1Free12|V1Free13|V1Free14|V1Free15|||||History1|Diagnose1|\r'
	ormMessage += 'ORC|CA|O1|||||^^^20100608065608^^normal^Test||20100607065608|^^^^^^|^^^^^^|mmustermann^Mustermann^Max^^^Prof.^MD|||20100608065608|^Test order |\r'
	ormMessage += 'OBR|1|O1||111^Test|||20100608065608|20100608065608|0|||||20100608065608||||||||20100608065608|||||^^^20100608065608^^normal^Test|||'
	return ormMessage

def oruSample():
	oruMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|199807311532||ORU^R01|3629|P|2.2\r'
	oruMessage += 'PID|2|2161348462|20809880170|1614614|20809880170^TESTPAT||19760924|M|||^^^^00000-0000|||||||86427531^^^03|SSN# HERE\r'
	oruMessage += 'ORC|NW|8642753100012^LIS|20809880170^LCS||||||19980727000000|||HAVILAND\r'
	oruMessage += 'OBR|1|8642753100012^LIS|20809880170^LCS|008342^UPPER RESPIRATORYCULTURE^L|||19980727175800||||||SS#634748641 CH14885 SRC:THROASRC:PENI|19980727000000||||||20809880170||19980730041800||BN|F\r'
	oruMessage += 'OBX|1|ST|008342^UPPER RESPIRATORY CULTURE^L||FINALREPORT|||||N|F||| 19980729160500|BN\r'
	oruMessage += 'ORC|NW|8642753100012^LIS|20809880170^LCS||||||19980727000000|||HAVILAND\r'
	oruMessage += 'OBR|2|8642753100012^LIS|20809880170^LCS|997602^.^L|||19980727175800||||G|||19980727000000||||||20809880170||19980730041800|||F|997602|||008342\r'
	oruMessage += 'OBX|2|CE|997231^RESULT 1^L||M415|||||N|F|||19980729160500|BN\r'
	oruMessage += 'NTE|1|L|MORAXELLA (BRANHAMELLA) CATARRHALIS\r'
	oruMessage += 'NTE|2|L| HEAVY GROWTH\r'
	oruMessage += 'NTE|3|L| BETA LACTAMASE POSITIVE\r'
	oruMessage += 'OBX|3|CE|997232^RESULT 2^L||MR105|||||N|F|||19980729160500|BN\r'
	oruMessage += 'NTE|1|L|ROUTINE RESPIRATORY FLORA'
	return oruMessage

def dftSample():
	dftMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|20100211073913||DFT^P03|DSD1184185250|P|2.5||||||\r'
	dftMessage += 'EVN||20100211073913||\r'
	dftMessage += 'PID|1|10476|10476^^^MR&1.3.6.1.4.1.21367.2005.1.1&ISO^MR^1.3.6.1.4.1.21367.2005.1.1&MR&ISO~999999999^^^^SS||Duck^Daffy||20100201|M|||123 Test St.^^Fort Wayne^IN^46125||||||||999999999|||||||||||\r'
	dftMessage += 'FT1|1|||20080528114700||CG|73630|||1||||||^^^^407^^^^TESTLOCATION||DICTATION||1^mie^mie^^^IN|||783933|1^mie^mie^^^IN|73630|RT~GA\r'
	dftMessage += 'PR1|1|CPT|73630||20080528114700|||||||1^mie^mie^^^IN||||RT~GA\r'
	dftMessage += 'DG1|1|ICD9|V76.12|Other Screening Mammogram for Malignant Neoplasm of Breast||F|||||||||0|1^mie^mie^^^IN|D\r'
	dftMessage += 'DG1|2|ICD9|959.7|Foot injury||F|||||||||0|1^mie^mie^^^IN|D'
	return dftMessage

def mostCommon():
	messageTypes = {"ACK" : "General acknowledgement",
	"ADT" : "Admit Discharge Transfer",
	"BAR" : "Billing Account Record",
	"DFT" : "Detailed Financial Transaction",
	"MDM" : "Medical Document Management",
	"MFN" : "Master Files Notification",
	"ORM" : "Order Message",
	"ORU" : "Observation Result",
	"QRY" : "Query",
	"RAS" : "Pharmacy/treatment administration",
	"RDE" : "Pharmacy/treatment encoded order",
	"RGV" : "Pharmacy/treatment give",
	"SIU" : "Scheduling Information Unsolicited"}
	return messageTypes

def getTime():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
	return st

def mllpSender(host, port, message):
	try:
		h = hl7.parse(message)
		messageType = mostCommon()
		with hl7.client.MLLPClient(host, port) as client:
			result = client.send_message(message)
			r = hl7.parse(result)
			if str(r[1][1]) == "AA": 
				print "[+] Message type accepted: " + str(h[0][9][0][0]) + " = " + messageType[str(h[0][9][0][0])]
			else: pass
	except:
		print "[-] MLLP sending failed."
		sys.exit()
		
def levelOne(host, port):
	messageTypes = ["ADT", "BAR", "DFT", "MDM", "MFN", "ORM", "ORU", "QRY", "RAS", "RDE", "RGV", "SIU"]
	for messageType in messageTypes:
		message = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|%s||%s^A01|MSG123|P|2.3||||AL|\r'%(getTime(), messageType)
		mllpSender(host, port, message)
	print "[+] Finished sending %s messages."%len(messageTypes)

def levelTwo(host, port):
	messages = [adtSample(), ormSample(), oruSample(), dftSample()]
	for message in messages:
		mllpSender(host, port, message)
	print "[+] Finished sending %s messages."%len(messages)

def fuzzer():
	script_name = os.path.basename(sys.argv[0])
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'host', type=str,
		help='host to connect to'
	)
	parser.add_argument(
		'port', type=int,
		help='port to connect to'
	)
	parser.add_argument(
		'level', type=str,
		help='"low", "high", "custom" for hl7 file input'
	)
	parser.add_argument(
		'-f', '--file', dest='filename',
		help='path to hl7 file'
	)
	args = parser.parse_args()
	if len(sys.argv) < 2:
		print "[-] Use --help for options"
		sys.exit()
	if args.host is not None:
		if args.port is not None:
			if args.level == "low":
				print "[+] Start level low"
				levelOne(args.host,args.port)
			elif args.level == "high":
				print "[+] Start level high"
				levelTwo(args.host,args.port)
			elif args.level == "custom":
				if args.filename is not None:
					with open(args.filename, 'rb') as f:
						stream = f.read()
						print "[+] Start level custom"
						mllpSender(args.host, args.port, stream)
						print "[+] Finished sending %s." %args.filename
			else:
				print "[-] Invalid Mode selected."

if __name__ == '__main__':
	fuzzer()
