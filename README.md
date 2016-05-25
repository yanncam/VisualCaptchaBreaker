# VisualCaptchaBreaker
**Breaking any VisualCaptcha.net with 100% success rate**

VisualCaptchaBreaker can be used against any VisualCaptcha 5.* web page (with API call "/start" and "/image"):
* http://visualcaptcha.net
* https://github.com/emotionLoop/visualCaptcha

In the VisualCaptcha branch 5.*, a [new protection mecanism](https://github.com/emotionLoop/visualCaptcha/issues/2) was introduced with adding random bytes to each PNG.

**VisualCaptchaBreaker convert these PNG to JPG to bypass this security.**

A 100% success rate can be obtained via a dictionary of all checksum (PNG and JPG) of each picture in the VisualCaptcha database (no need OCR nor specific image-library analysis).

Tested successfully against :
* [VisualCaptcha demo page](http://demo.visualcaptcha.net/)
* Custom VisualCaptcha PoC with simple POST data
* Custom VisualCaptcha PoC with POST multipart/form-data.

## Demonstration video
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/fkfeDQqXNdk/0.jpg)](https://www.youtube.com/watch?v=fkfeDQqXNdk)

## How to use VisualCaptchaBreaker
```shell
$ python VisualCaptchaBreaker-latest.py -h

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

Title:                  VisualCaptchaBreaker.py  Version: 1.0.0
Author:                 Yann CAM
Website:                www.asafety.fr
Source:                 github.com/yanncam/VisualCaptchaBreaker
Description:            Breaking any VisualCaptcha 5.x with 100% success rate
-----------------------------------------------------------------------------

usage: VisualCaptchaBreaker-latest.py [OPTIONS]

Breaking any VisualCaptcha 5.x with 100% success rate :
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

        %VISUALCAPTCHANAME%=%VISUALCAPTCHAVALUE%&submit-bt=

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Number of request(s) to make (default: 1)
  -s STARTPATH, --startPath STARTPATH
                        VisualCaptcha initialization path (default: /start)
  -i IMAGEPATH, --imagePath IMAGEPATH
                        VisualCaptcha image path (default: /image)
  -c, --cookie          Use cookie defined in raw HTTP file(s)
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files containing raw HTTP requests with %VISUALCAPTCHANAME% and %VISUALCAPTCHAVALUE% as POST param
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing raw HTTP requests in files with %VISUALCAPTCHANAME% and %VISUALCAPTCHAVALUE% as POST param
  -p PROXY, --proxy PROXY
                        HTTP Proxy to send requests via. (Burp eg: 127.0.0.1:8080)
  --https               Use HTTPS
  -v, --verbose         Debug logging
```

## Customize VisualCaptchaBreaker dictionary database
VisualCaptchaBreaker python script embed a picture database generated from the 37 default images of VisualCaptcha with their corresponding text-label (english and french), JPG checksum and PNG checksum.

If an implementation of VisualCaptcha use custom picture database, you need to define your own dictionary.

Use these script to create one :
* scripts/01-enum_VisualCaptcha_texts.py
* scripts/02-download_VisualCaptcha_png_db.py
* scripts/03-convert_VisualCaptcha_imgdb_png2jpg.py
* scripts/04-calculate_VisualCaptcha_img_checkSum.py

Then update the dictionary structure in the "VisualCaptchaBreaker" Python script as follow :

```python
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
[...]
```

## Ideas for the future...

* Adding auto-detect endpoints "/start" and "/image" (if their path are customized)
* Adding other language for default text-label
* Integrate audio-captcha breaking with the same methodology
* Implement statistics to display breaking rate in real time
* Manage better exception and error message
* Create an all-in-one script to generate a custom image dictionary with Python syntaxe

## Misc

Greetz to [St0rn](http://0xbadcoded.com/), [nj8](http://www.information-security.fr/) and [Emiya](http://www.georgestaupin.com/)
