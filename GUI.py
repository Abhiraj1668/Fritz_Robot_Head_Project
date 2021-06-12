## Import all required libraries
import os
import serial
import json
import time
import pygame
import math
import os
from pygame import mixer
import serial.tools.list_ports

## Initialize stuffs
pygame.init()
mixer.init()

## Current Directory
cDir= os.getcwd()

portse= 0
## Screen and its elements
width= 800
height= 600
screen= pygame.display.set_mode((width,height))

## Gesture Buttons Dimensions
vBtnHeight= 30
vBtnWidth= 250
vBtnX= 50
vBtnY= 50

## Gesture Button Variables
vBtnsCnt=0
vBtns=[]
vBtnDict={}
pageNo= 0
page= slice(0,10)

## Gesture Page Scroll Buttons
nxtBtn= pygame.Rect(700,250,50,30) #x,y,w,h
preBtn= pygame.Rect(700,200,50,30) #x,y,w,h


## Expression Buttions Dimensions
eBtnHeight= 30
eBtnWidth= 250
eBtnX= 50
eBtnY= 400

## Expression Button Variables
eBtnsCnt=0
eBtns=[]
eBtnDict={}
epageNo= 0
epage= slice(0,8)

## Expression Page Scroll Buttons
nxteBtn= pygame.Rect(700,500,50,30) #x,y,w,h
preeBtn= pygame.Rect(700,550,50,30) #x,y,w,h


## Initialize Gesture Buttons
def initvBtns(libFile):
    global vBtnsCnt
    vBtnsCnt= 0
    vBtns.clear()
    vBtnDict.clear()
    ## Read All names of gestures present in the library
    for keys in libFile:
        vBtnsCnt= vBtnsCnt + 1
        ## Divide the list in set of 5s
        if (vBtnsCnt-1)%10 < 5:
            ## 1st 5 button display one below another on left side of the window
            vBtns.append(pygame.Rect(vBtnX , vBtnY+ ((vBtnsCnt-1)%5)*50, vBtnWidth, vBtnHeight))
            pass
        else:
            ## next 5 buttons display one below another on right side of the window
            vBtns.append(pygame.Rect(vBtnX + 350,  vBtnY + ((vBtnsCnt-1)%5)*50, vBtnWidth, vBtnHeight))
            pass
        vBtnDict[keys]= vBtns[vBtnsCnt-1]
    return


## Initialize Expression Buttions
def initeBtns(libFile):
    global eBtnsCnt
    eBtnsCnt= 0
    eBtns.clear()
    eBtnDict.clear()
    ## Read All names of emotions present in the library
    for keys in libFile:
        eBtnsCnt= eBtnsCnt + 1
        ## Divide the list in set of 4s
        if (eBtnsCnt-1)%8 < 4:
            ## 1st 4 button display one below another on left side of the window
            eBtns.append(pygame.Rect(eBtnX , eBtnY+ ((eBtnsCnt-1)%4)*50, eBtnWidth, eBtnHeight))
            pass
        else:
            ## next 4 buttons display one below another on right side of the window
            eBtns.append(pygame.Rect(eBtnX + 350,  eBtnY + ((eBtnsCnt-1)%4)*50, eBtnWidth, eBtnHeight))
            pass
        eBtnDict[keys]= eBtns[eBtnsCnt-1]
    return


## The main function
def main():
    global pageNo
    global page
    global epageNo
    global epage
    global portse
    ## Is program running
    running= True
    ## Get list of serial Com ports connected to PC
    portse = serial.tools.list_ports.comports()
    cnt= 1
    ## Display the list of all com ports on to command line
    for port in portse:
        print("{}) {}".format(cnt, port.name))
    ## Ask user to select arduino com port
    portNo= int(input("Select COM Port by number: ")) - 1
    ## Load Gesture library file
    with open(cDir + '/library.json') as f:
        data= f.read()
    ## convert json to python dictionary
    library= json.loads(data)
    ## initialize gesture buttons
    initvBtns(libFile= library)
    ## Load Expression library file
    with open(cDir + '/expLibrary.json') as f:
        data= f.read()
    elibrary= json.loads(data)
    ## Load Expression buttons
    initeBtns(libFile= elibrary)
    ## Try to connect to COM port specified by user
    try:
        arduino= serial.Serial(port=portse[portNo].name, baudrate=57600, timeout=0.1)
    except:
        ## If unable to connect, show error message and exit
        print("Unable to connect to Arduino. Please Check Connections and COM Port!!!")
        time.sleep(5)
        return
    ## Start Looping the GUI window
    while running:
        for btns in vBtns[page]:
            ## Draw all gesture buttons
            drawRect(btns)
            ## Write corresponding text into gesture buttons
            createText(getKey(vBtnDict, btns, pageNo, 10), btns)
        for btns in eBtns[epage]:
            ## draw all expression buttions
            drawRect(btns)
            ## Write corresponding text into expression buttions
            createText(getKey(eBtnDict, btns, epageNo, 8), btns)
        ## Draw Scroll buttons and write text into it for gesture
        drawRect(nxtBtn)
        createText(">>", nxtBtn)
        drawRect(preBtn)
        createText("<<", preBtn)
        ## Draw Scroll buttons and write text into it for expressions
        drawRect(nxteBtn)
        createText(">>", nxteBtn)
        drawRect(preeBtn)
        createText("<<", preeBtn)
        ## Update the display with all buttons drawn
        pygame.display.update()

        ## Check for any event occured on the window
        for event in pygame.event.get():
            ## If quit pressed
            if event.type== pygame.QUIT:
                running= False
                pass
            
            ## If left clicked on button
            if event.type== pygame.MOUSEBUTTONDOWN and event.button==1 :
                ## Check if clicked on any of the gesture buttons
                for btns in vBtns[page]:
                    if btns.collidepoint(event.pos):
                        ## If clicked on a gesture button, play music corresponding to that button pressed, by getting its data from dictionary
                        playMusic(library[getKey(vBtnDict, btns, pageNo, 10)]['fname'])
                        ## Start sending commands to arduino to show postures
                        doGestures(btns, library, arduino, pageNo)

                ## Check if clicked on any of the expression buttons
                for btns in eBtns[epage]:
                    if btns.collidepoint(event.pos):
                        ## If clicked on a gesture button, Start sending commands to arduino to show expression
                        doeGestures(btns, elibrary, arduino, epageNo)

                ## If previous gesture page button pressed
                if preBtn.collidepoint(event.pos):
                    ## Check if gesture page number is greater than 0
                    if pageNo > 0:
                        ## If greater that 0, decrement the gesture page number
                        pageNo= pageNo - 1
                    else:
                        ## Otherwise keep it 0
                        pageNo= 0
                    ## Update the slice to be used later for draw buttons
                    page= slice(10*pageNo, 10*pageNo + 10)
                ## If next gesture page button pressed
                if nxtBtn.collidepoint(event.pos):
                    ## If page number is equal or greater than max page number
                    if pageNo >= (math.ceil(vBtnsCnt/10) -1):
                        ## Set page number to max page number
                        pageNo= math.ceil(vBtnsCnt/10) -1
                    else:
                        ## Otherwise increment gesture page number
                        pageNo= pageNo +1
                    ## Update slice to be used later for draw buttons
                    page= slice(10*pageNo,10*pageNo+10)

                ## If previous expression page button pressed
                if preeBtn.collidepoint(event.pos):
                    ## Check if expression page number is greater than 0
                    if epageNo > 0:
                        ## Decrement expression page number
                        epageNo= epageNo - 1
                    else:
                        ## Otherwise keep the expression page number 0
                        epageNo= 0
                    ## Update page number slice for later
                    epage= slice(8*epageNo, 8*epageNo + 8)
                ## If next expression page button pressed
                if nxteBtn.collidepoint(event.pos):
                    ## If page number is equal or greater than max page number
                    if epageNo >= (math.ceil(eBtnsCnt/10) -1):
                        ## Set page number to max page number
                        epageNo= math.ceil(eBtnsCnt/10) -1
                    else:
                        ## Increment page number
                        epageNo= epageNo +1
                    ## Update page number slice for later
                    epage= slice(8*epageNo,8*epageNo+8)

            pass

        ## Screen background color as white
        screen.fill((255,255,255))

    ## If quit, exit program completely    
    pygame.quit()

## Function to draw rectangle on window
def drawRect(btn):
    ## Draws rectangle with required dimentions and coordinates in Red color
    pygame.draw.rect(screen, (255,0,0), btn)
    return

## Function to load and start playing the music file
def playMusic(mFile):
    ## Try to play music by file and location provided in parameter
    try:
        ## Load the audio file
        mixer.music.load(mFile)
        ## Play the audio file
        mixer.music.play()
    except:
        pass
    pass

## Create Text on the button
def createText(txt, rectPos):
    ## Setup text font
    font= pygame.font.Font('freesansbold.ttf',20)
    ## Render text in a variable with required color
    sType= font.render(txt, True, (0,255,255))
    ## Integrate the text and the corresponding button
    screen.blit(sType, rectPos)
    pass

## Get Key, that is the gesture name from the dictionary 
def getKey(dict, val, pageNo, multplr):
    return list(dict.keys())[list(dict.values()).index(val)+ multplr*pageNo]

## Send commands to arduino to show gestures
def doGestures(btnPressed, library, arduino, pageNo):
    global portse
    ## Get gesture name which need to be replicated on to the robot head
    ky= getKey(vBtnDict, btnPressed, pageNo, 10)
    ## Play the audio file corresponding to the button
    playMusic("{}/AudioFiles/{}".format(cDir,library[ky]['fname']))
    iTime=-1
    playPos= 0
    ## helper dictionary to parse library file
    partDict= {"eb1": "ga", "eb2": "gb", "el1": "gc", "el2": "gd", "ey1": "ge", "ey2": "gf", "ey3": "gh", "ey4": "gi", "li1": "gj", "li2": "gk", "li3": "gl", "ne1": "gm", "ne2": "gn"}
    ## While audio file is still playing
    while mixer.music.get_busy():
        try:
            arduino= serial.Serial(port=portse[portNo].name, baudrate=57600, timeout=0.1)
        except:
            # print("Unable to connect to Arduino. Please Check Connections and COM Port!!!")
            pass
        ## Get time position audio has been playing in ms
        pos= mixer.music.get_pos()
        try:
            ## Find matching time or time frame in gesture file that has been just passed the time of audio playing
            if library[ky]['sync'][playPos]['time'] > pos:
                continue
            else:
                ## Get all items of the corresponding time posture
                for keys, vals in library[ky]['sync'][playPos].items():
                    if keys != "time":
                        ## Send appropriate commands to arduino to show posture by moving appropriate motors
                        arduino.write(bytes('{}{}'.format(partDict[keys],vals),'utf-8'))
                ## Go to next posture    
                playPos = playPos + 1
        except:
            continue

## Send commands to arduino to show expressions
def doeGestures(btnPressed, library, arduino, pageNo):
    ## Get expression name which need to be replicated on to the robot head
    ky= getKey(eBtnDict, btnPressed, pageNo, 8)
    ## helper dictionary to parse library file
    partDict= {"eb1": "ga", "eb2": "gb", "el1": "gc", "el2": "gd", "ey1": "ge", "ey2": "gf", "ey3": "gh", "ey4": "gi", "li1": "gj", "li2": "gk", "li3": "gl", "ne1": "gm", "ne2": "gn"}
    try:
        ## Get all items of the corresponding time posture
        for keys, vals in library[ky].items():
            if keys != "time":
                ## Send appropriate commands to arduino to show posture by moving appropriate motors
                arduino.write(bytes('{}{}'.format(partDict[keys],vals),'utf-8'))                        
    except:
        pass

if __name__ == '__main__':
    ##Run this script only if running as main
    main()