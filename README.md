# UberPollCheckPrice

![full](https://raw.githubusercontent.com/DeqingSun/UberPollCheckPrice/master/checkPrice.gif)

This project fetches real time price from Uber to help you understand When is the best time to take a Uber back home without paying extra.

You need to enable USB Debugging mode.

on Mac

brew install tesseract
brew install android-platform-tools

https://pypi.python.org/pypi/pytesseract/0.1
http://effbot.org/downloads/Imaging-1.1.7.tar.gz
sudo python setup.py install

on Win7

Tesseract:
https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download
ADB:
https://forum.xda-developers.com/showthread.php?t=2588979
Perl:
https://www.perl.org/get.html

pip install pytesseract
http://effbot.org/media/downloads/PIL-1.1.7.win32-py2.7.exe




adb shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > screen.png

adb shell screencap -p > screen.png

adb shell input keyevent KEYCODE_BACK



On android Turn on adb

