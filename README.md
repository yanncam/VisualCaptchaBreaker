# VisualCaptchaBreaker
Breaking any VisualCaptcha.net with 100% success rate

```shell
# python VisualCaptchaBreaker-latest.py -h

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
