import time
import signal
import datetime
import sys
import socket
import hl7
import Tkinter
import tkFileDialog
from hl7.client import MLLPClient
from colorama import init, Fore
from pathlib import Path

init(autoreset=True)

class Messages():
	def most_common(self):
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

	def adtSample(self):
		adtMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|||ADT^A01|MSG123|P|2.2||||AL|\r'
		adtMessage += 'PID|||P1||Lastname1^Firstname1^MiddleName1^^^Degree1|MotherMaidenName1|19720828|M|||Street 123^^New York^^12345||0049123456789||||||SSN1||||||||^Occupation1\r'
		adtMessage += 'PV1|1|O|Room 123|||||^Smith^John^^^^MD|||||||||||V1|20100607065608|||||||||||||||||||ServicingFacility1|||||20100608065608\r'
		adtMessage += 'IN1|1|111||Insurance\r'
		adtMessage += 'ZPI|V1Free1|V1Free2|V1Free3|V1Free4|V1Free5|V1Free6|V1Free7|V1Free8|V1Free9|V1Free10|V1Free11|V1Free12|V1Free13|V1Free14|V1Free15|||||History1|Diagnose1|'
		return adtMessage
	
	def ormSample(self):
		ormMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|20100607065608||ORM^O01|MSG123|P|2.2||||AL|\r'
		ormMessage += 'PID|||P1||Lastname1^Firstname1^MiddleName1^^^Degree1|MotherMaidenName1|19720828|M|||Street 123^^New York^^12345||0049123456789||||||SSN1||||||||^Occupation1\r'
		ormMessage += 'PV1|1|O|Room 123|||||^Lastname2^Firstname2^^^^MD|||||||||||V1||||||||||||||||||||ServicingFacility1|||||20100608065608\r'
		ormMessage += 'IN1|1|111||Insurance\r'
		ormMessage += 'ZPI|V1Free1|V1Free2|V1Free3|V1Free4|V1Free5|V1Free6|V1Free7|V1Free8|V1Free9|V1Free10|V1Free11|V1Free12|V1Free13|V1Free14|V1Free15|||||History1|Diagnose1|\r'
		ormMessage += 'ORC|CA|O1|||||^^^20100608065608^^normal^Test||20100607065608|^^^^^^|^^^^^^|mmustermann^Mustermann^Max^^^Prof.^MD|||20100608065608|^Test order |\r'
		ormMessage += 'OBR|1|O1||111^Test|||20100608065608|20100608065608|0|||||20100608065608||||||||20100608065608|||||^^^20100608065608^^normal^Test|||'
		return ormMessage

	def oruSample(self):
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

	def dftSample(self):
		dftMessage = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|20100211073913||DFT^P03|DSD1184185250|P|2.5||||||\r'
		dftMessage += 'EVN||20100211073913||\r'
		dftMessage += 'PID|1|10476|10476^^^MR&1.3.6.1.4.1.21367.2005.1.1&ISO^MR^1.3.6.1.4.1.21367.2005.1.1&MR&ISO~999999999^^^^SS||Duck^Daffy||20100201|M|||123 Test St.^^Fort Wayne^IN^46125||||||||999999999|||||||||||\r'
		dftMessage += 'FT1|1|||20080528114700||CG|73630|||1||||||^^^^407^^^^TESTLOCATION||DICTATION||1^mie^mie^^^IN|||783933|1^mie^mie^^^IN|73630|RT~GA\r'
		dftMessage += 'PR1|1|CPT|73630||20080528114700|||||||1^mie^mie^^^IN||||RT~GA\r'
		dftMessage += 'DG1|1|ICD9|V76.12|Other Screening Mammogram for Malignant Neoplasm of Breast||F|||||||||0|1^mie^mie^^^IN|D\r'
		dftMessage += 'DG1|2|ICD9|959.7|Foot injury||F|||||||||0|1^mie^mie^^^IN|D'
		return dftMessage

	def builtin_message_types(self):
		message_types = ["ADT", "ORM", "ORU", "DFT"]
		return message_types

	def get_builtin_message(self, message_type):
		if message_type == "ADT":
			return self.adtSample()
		elif message_type == "ORM":
			return self.ormSample()
		elif message_type == "ORU":
			return self.oruSample()
		elif message_type == "DFT":
			return self.dftSample()

class Timeout():
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

class Target:
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def checkPort(self):
		print (Fore.MAGENTA + "*** Checking if {0}:{1} is available ***".format(self.host, self.port))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		try:
			s.connect((self.host,int(self.port)))
			s.shutdown(2)
			print (Fore.GREEN + "*** Specified Host and port reachable ***")
			return True
		except:
			print (Fore.RED + "*** Specified Host and port not reachable ***")
			return False

class Attacker():
	def manual(self, target):
		print (Fore.MAGENTA + "*** Starting Manual attacker ***")
		print (Fore.YELLOW + "Injection point syntax example Firstname: PID.0.5.0.1.0")
		injectPoint = raw_input("Injection point: [PID.0.5.0.1.0] ")
		if not injectPoint:
			injectPoint = "PID.0.5.0.1.0"
		elif len(injectPoint.split(".")) != 6:
			print (Fore.RED + "*** Invalid injection point defined ***")
			self.manual(target)
		payload = raw_input("Payload: ")
		if not payload:
			payload = "foo"
		messageSource = raw_input("Message source [builtin, file]: [builtin] ")
		if messageSource.upper() == "FILE":
			Tkinter.Tk().withdraw()
			sourceFile = tkFileDialog.askopenfilename()
			if len(sourceFile) > 1:
				with open(sourceFile, "r") as file:
					message = file.read().replace("\r", "\n")

				response = self.send_mllp(target.host, target.port, message_after_builder)
				self.analyse_responses_auto(response, payload, message_after_builder)
			else:
				print (Fore.RED + "*** Invalid source file defined ***")
				sys.exit()
		else:
			messageTypes = Messages().builtin_message_types()
			messageTypeSelected = raw_input("Select message type {0}: [ADT] ".format(messageTypes))
			if not messageTypeSelected:
				messageTypeSelected = "ADT"
			if messageTypeSelected.upper() in messageTypes:
				message = Messages().get_builtin_message(messageTypeSelected.upper())
				message_after_builder = self.message_builder_manual(message, payload, injectPoint)
				response = self.send_mllp(target.host, target.port, message_after_builder)
				self.analyse_responses_auto(response, payload, message_after_builder)
			else:
				print (Fore.RED + "*** Invalid message type selected ***")

	def message_builder_manual(self, message, payload, injectPoint):
		try:
			h = hl7.parse(message)
			split = injectPoint.split('.')
			h.segments(split[0])[int(split[1])][int(split[2])][int(split[3])][int(split[4])] = payload
		except:
			print (Fore.RED + "*** Something went wrong while message building. Check injection point syntax and message ***")
			sys.exit()
		return h

	def auto(self, target):
		print (Fore.MAGENTA + "*** Starting Auto attacker ***")
		messageSource = raw_input("Message source [builtin, file]: [builtin] ")
		responses = []
		if messageSource.upper() == "FILE":
			Tkinter.Tk().withdraw()
			sourceFile = tkFileDialog.askopenfilename()
			if len(sourceFile) > 1:
				with open(sourceFile, "r") as file:
					print file.read()
			else:
				print (Fore.RED + "*** Invalid source file defined ***")
				sys.exit()
		else:
			messageTypes = Messages().builtin_message_types()
			messageTypeSelected = raw_input("Select message type {0}: [ADT] ".format(messageTypes))
			if not messageTypeSelected:
				messageTypeSelected = "ADT"
			if messageTypeSelected.upper() in messageTypes:
				message = Messages().get_builtin_message(messageTypeSelected.upper())
		payloadMode = raw_input("Payload [man, builtin, file]: [man] ")
		if payloadMode.upper() == "BUILTIN":
			return True
		elif payloadMode.upper() == "FILE":
			Tkinter.Tk().withdraw()
			payloadFile = tkFileDialog.askopenfilename()
			if len(payloadFile) > 1:
				with open(payloadFile, "r") as file:
					for line in file:
						payload = line.strip()
						self.inject_point_generator(target, message, payload)
			else:
				print (Fore.RED + "*** Invalid source file defined ***")
				sys.exit()
		else:
			payloadMan = raw_input("Payload: ")
			if not payloadMan:
				payloadMan = "foo"
			self.inject_point_generator(target, message, payloadMan)

		if responses:
			checkResponses = raw_input("Analyse responses [Y, N]? [Y] ")
			if checkResponses.upper() == "Y":
				self.analyse_responses_auto(response, payload)
			else:
				sys.exit()
		return True
	

	def analyse_responses_auto(self, response, payload, message):
		keywords = ["ERROR", "EXCEPTION", "SQL", "JSON", "XML"]
		for keyword in keywords:
			if keyword.upper() in response.upper():
				print (Fore.GREEN + "*** Error based Keyword in response ***")
				print (Fore.YELLOW + "Message segment: \n{0}".format(message))
				print (Fore.YELLOW + "Keyword: {0}".format(keyword))
				print (Fore.YELLOW + "Response: {0}".format(response))
				stopQuestion = raw_input("Stop attack [Y, N]? [N] ")
				if stopQuestion.upper() == "Y":
					sys.exit()
		if payload.upper() in response.upper():
			print (Fore.GREEN + "*** Payload reflected in response ***")
			print (Fore.YELLOW + "Message segment: \n{0}".format(message))
			print (Fore.YELLOW + "Paload: {0}".format(payload))
			print (Fore.YELLOW + "Response: {0}".format(response))
			stopQuestion = raw_input("Stop attack [Y, N]? [N] ")
			if stopQuestion.upper() == "Y":
				sys.exit()
		return True

	def inject_point_generator(self, target, message, payload):
		messageCounter = 0
		segment = 0
		field = 0
		repetition = 0
		component = 0
		sub_component = 0
		responses = []
		#try:
		h = hl7.parse(message)
		for segment in range(1, len(h)+1):
			for field in range(1, len(h(segment))):
				for repetition in range(0, len(h(segment)[field])):
					if "^" in str(h(segment)[field][repetition]):
						temp = h(segment)[field][repetition]
						splited = str(h(segment)[field][repetition]).split("^")
						for i in range(0, len(splited)):
							tempSplited = splited[i]
							splited[i] = payload
							finalString = ""
							for j in range(0, len(splited)):
								finalString += splited[j] + "^"
							splited[i] = tempSplited
							h(segment)[field][repetition] = finalString[:-1]
							response = self.send_mllp(target.host, target.port, h)
							self.analyse_responses_auto(response, payload, h(segment))
							messageCounter += 1
							h(segment)[field][repetition] = temp
					else:
						temp = h(segment)[field][repetition]
						h(segment)[field][repetition] = payload
						response = self.send_mllp(target.host, target.port, h)
						self.analyse_responses_auto(response, payload, h(segment))
						messageCounter += 1
						h(segment)[field][repetition] = temp
		print (Fore.GREEN + "*** {0} messages sent ***".format(messageCounter))
		
	def send_mllp(self, host, port, message):
		if type(message) is str: 
			h = hl7.parse(message)
		else:
			h = message
		messageType = Messages().most_common()
		with hl7.client.MLLPClient(host, int(port)) as client:
			response = client.send_message(message)
			r = hl7.parse(response)
			if r:
				if str(r[1][1]) == "AA": 
					print (Fore.GREEN + "*** ACK received ***")
					client.close()
				else: 
					print (Fore.RED + "*** No ACK received ***")
					client.close()
			else:
				print (Fore.RED + "*** No response received ***")
				client.close()
		return response

class Fuzzer():
	def simple(self, target):
		print (Fore.MAGENTA + "*** Starting MSH fuzzer ***")
		messageTypes = ["ADT", "BAR", "DFT", "MDM", "MFN", "ORM", "ORU", "QRY", "RAS", "RDE", "RGV", "SIU"]
		eventTypes = ["A01", "O01", "P03", "P01", "T02", "M02", "R01", "A19", "O17", "O11", "O15", "S12"]
		for messageType in messageTypes:
			for messageEvent in eventTypes:
				message = 'MSH|^~\&|HISSERVER|HISVENDOR|FUZZER|TEST|{0}||{1}^{2}|MSG123|P|2.3||||AL|\r'.format(self.get_time(), messageType, messageEvent)
				self.send_mllp(target.host, target.port, message)
		print (Fore.YELLOW + "[+] Finished sending {0} messages.".format(len(messageTypes) * len(eventTypes)))
		sys.exit()

	def complex(self, target):
		print (Fore.MAGENTA + "*** Starting FULL fuzzer ***")
		messageObject = Messages()
		messages = [messageObject.adtSample(), messageObject.ormSample(), messageObject.oruSample(), messageObject.dftSample()]
		for message in messages:
			self.send_mllp(target.host, target.port, message) 
		print (Fore.YELLOW + "[+] Finished sending {0} messages.".format(len(messages)))

	def get_time(self):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
		return st

	def send_mllp(self, host, port, message):
		if type(message) is str: 
			h = hl7.parse(message)
		else:
			h = message
		messageType = Messages().most_common()
		with hl7.client.MLLPClient(host, int(port)) as client:
			response = client.send_message(message)
			r = hl7.parse(response)
			if str(r[1][1]) == "AA": 
				print (Fore.GREEN + "[+] Message type accepted: " + str(h[0][9][0][0]) + "^" + str(h[0][9][0][1]) + " = " + messageType[str(h[0][9][0][0])])
				client.close()
			else: 
				pass

class Kraken():
	print """  _    _ _      ______ _  __          _              
 | |  | | |    |____  | |/ /         | |             
 | |__| | |        / /| ' / _ __ __ _| | _____ _ __  
 |  __  | |       / / |  < | '__/ _` | |/ / _ \ '_ \ 
 | |  | | |____  / /  | . \| | | (_| |   <  __/ | | |
 |_|  |_|______|/_/   |_|\_\_|  \__,_|_|\_\___|_| |_|
  by mez [modzero.ch]                               """
	if len(sys.argv) != 3:
		print (Fore.RED + "*** Usage: {0} [Host IP] [Host Port]".format(sys.argv[0]))
		sys.exit()
	else:
		host = sys.argv[1]
		if "-" in sys.argv[2]:
			split = sys.argv[2].split("-")
			ports = []
			for port in range(int(split[0]), int(split[1])+1):
				ports.append(port)
			print ports
			for port in ports:
				target = Target(host, port)
				if not target.checkPort():
					pass
				else:
					mode = raw_input("Mode [FUZZ, ATTACK]? [FUZZ] ")
					if mode.upper() == "ATTACK":
						module = raw_input("Module [MANUAL, AUTO]? [AUTO] ")
						if module.upper() == "MANUAL":
							Attacker().manual(target)
						else:
							Attacker().auto(target)
					else:
						module = raw_input("Module [MSH, FULL]? [MSH] ")
						if module.upper() == "FULL":
							Fuzzer().complex(target)
						else:
							Fuzzer().simple(target)
			sys.exit()
		target = Target(host, sys.argv[2])
		if not target.checkPort():
			sys.exit()
		else:
			mode = raw_input("Mode [FUZZ, ATTACK]? [ATTACK] ")
			if mode.upper() == "FUZZ":
				module = raw_input("Module [MSH, FULL]? [MSH] ")
				if module.upper() == "FULL":
					Fuzzer().complex(target)
				else:
					Fuzzer().simple(target)
			else:
				module = raw_input("Module [MANUAL, AUTO]? [AUTO] ")
				if module.upper() == "MANUAL":
					Attacker().manual(target)
				else:
					Attacker().auto(target)

if __name__ == '__main__':
	Kraken()
