from PIL import Image 
from pytesseract import *
import os
import re
from datetime import datetime

destLabel = 'Work'
priceLogFile= open("priceLog.txt","w+")

while True:
    while True:    #request price by match string
        os.system("adb shell screencap -p > screen.png")
    
        rawImg = Image.open('screen.png')
        processImg = Image.new("RGB", (rawImg.size[0],rawImg.size[1]/2), (255,255,255))    #need a RGB instead of RGBA
        
        #print (str(im.size[0]) + " " + str(im.size[1]) + str(-im.size[1]/2))
        
        
        processImg.paste(rawImg,(0,(-rawImg.size[1]/2)))   ##only bottom half
        boxes = image_to_string(processImg,lang='eng',boxes=True)
        #print boxes;
        
        #print '=========';
        
        recongnizedIndex = 0
        x=0
        y=0
        for box in boxes.splitlines():  #find string
            if recongnizedIndex<len(destLabel) and box[0] == destLabel[recongnizedIndex]:
                recongnizedIndex=recongnizedIndex+1
                if recongnizedIndex==len(destLabel):
                    para = box.split(' ')
                    x=int(para[1])
                    y=rawImg.size[1]-int(para[4])
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


