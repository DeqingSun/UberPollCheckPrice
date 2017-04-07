from PIL import Image 
from pytesseract import *
import os
import re
from datetime import datetime

destLabel = 'Home'
priceLogFile= open("priceLog.txt","a")
convert_OD_to_0A='\r\r\n'   #console may add line end on stream. I used '\r\r\n' on Win7 with Nexus 5X, '\r\n' on Win7 with Nexus 5 and '\n' on Mac with Nexus 5X

while True:
    while True:    #request price by match string
        os.system("adb shell screencap -p > screen.png")

        if convert_OD_to_0A!='\n':
            with open('screen.png','rb') as infile:
                data=infile.read().replace(convert_OD_to_0A, '\n')
            with open('screenOut.png', 'wb') as outfile:
                outfile.write(data)
            os.unlink('screen.png')
            os.rename('screenOut.png', 'screen.png')
    
        rawImg = Image.open('screen.png')
        processImg = Image.new("RGB", (rawImg.size[0],int(rawImg.size[1]*.32)), (255,255,255))    #need a RGB instead of RGBA
        processImg.paste(rawImg,(0,(-rawImg.size[1]/2)))   ##only bottom half without ad, ad banner will interfere API

        processImg=processImg.convert('L'); #grayscale
        
        w, h = processImg.size
        for xPix in range(w):
            for yPix in range(h):
                if processImg.getpixel((xPix, yPix)) > 10: #threshold
                    processImg.putpixel((xPix, yPix), 255)
        
        boxes = image_to_string(processImg,lang='eng',boxes=True)
        
        recongnizedIndex = 0
        x=0
        y=0
        for box in boxes.splitlines():  #find string
            if recongnizedIndex<len(destLabel) and box[0] == destLabel[recongnizedIndex]:
                recongnizedIndex=recongnizedIndex+1
                if recongnizedIndex==len(destLabel):
                    para = box.split(' ')
                    x=int(para[1])
                    y=rawImg.size[1]/2+processImg.size[1]-int(para[4])
                    print 'Found '+destLabel+' on '+str(x)+', '+str(y)
            else:
                recongnizedIndex=0
        
        if x>0 and y>0 :
            print 'Click '+destLabel+' on '+str(x)+', '+str(y)
            os.system("adb shell input tap "+str(x)+" "+str(y)) #get price
            break;
        else:
            print 'String: '+destLabel+' not found on screen, try again'
        
        
    while True:
        os.system("adb shell screencap -p > screen.png")
    
        if convert_OD_to_0A!='\n':
            with open('screen.png','rb') as infile:
                data=infile.read().replace(convert_OD_to_0A, '\n')
            with open('screenOut.png', 'wb') as outfile:
                outfile.write(data)
            os.unlink('screen.png')
            os.rename('screenOut.png', 'screen.png')
    
        rawImg = Image.open('screen.png')
        processImg = Image.new("RGB", (rawImg.size[0],rawImg.size[1]/2), (255,255,255))    #need a RGB instead of RGBA
    
        processImg.paste(rawImg,(0,(-rawImg.size[1]/2)))   ##only bottom half
        text = image_to_string(processImg,lang='eng',boxes=False)
        
        pattern = re.compile(r"(\$)(\d+\.\d*)")
        match = pattern.search(text)
        if match:
            print 'Uber poll cost ' + match.groups()[1] + ' on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            priceLogFile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+','+match.groups()[1]+'\n')
            priceLogFile.flush();
            print 'Press back button'
            os.system('adb shell input keyevent KEYCODE_BACK') 
            break;
        else:
            print 'No price found, try again'


