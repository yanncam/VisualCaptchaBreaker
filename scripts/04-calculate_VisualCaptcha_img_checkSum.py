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

- 	Help script to display checkSum of all pictures in specified directory.
	Configure "imgDir" with all existing directory that contains img.
	Be carefull ! Newer version of VisualCaptcha integrate random bytes in PNG file. So checkSum can be different between two PNG databases.
	JPG checkSum are always the sames.

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
from os import listdir
from os.path import isfile, join
import hashlib

imgDir = ["./imgPng", "./imgJpg"]

for dir in imgDir:
	imgFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	for img in imgFiles:
		hash = hashlib.md5(open(dir + "/" + img, 'rb').read()).hexdigest()
		print "[+] checkSum of [" + dir + "/" + img + "] is [" + hash + "]"
