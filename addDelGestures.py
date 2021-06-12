## import all required libraries
import numpy as np
import json
import os
import time
import sys
from os import system, name
  
dictLoad= {}
addDict= {}

## Current Directory
cDir= os.getcwd()

# define our clear function
def clear():  
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


## Load gesture library file
def loadLibrary():
    global dictLoad
    with open(cDir + '/library.json') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    dictLoad = json.loads(data)

## Functions displays all loaded gestures from library to the command line
def displayAllGestures():
    counter= 1
    print("0) NONE")
    for key in dictLoad:
        print("{}) {}".format(counter, key))
        counter += 1
    return

## This function delets gesture from library file
def delGesture():
    counter= 1
    ## Get gesture number from the user to be deleted
    delKey= int(input("Enter Number of gesture to be deleted: "))
    for key in dictLoad:
        ## delete the corresponding gesture from library and update the library file
        if counter== delKey:
            del dictLoad[key]
            print("Delete Successful")
            break
        counter += 1
    return

## This function writes the updated local dictionary to the library file
def updateFile():
    with open('{}/library.json'.format(cDir), 'w') as fp:
        json.dump(dictLoad, fp)
    print("Update Succssful")
    return

## This function helps user to add new gesture to the library file
def addGesture():
    global addDict
    global dictLoad
    ## Important notice for user
    print("IMPORTANT NOTE: ENTER TIMES STAMPS SEQUENTIALLY FOR THE GESTURE TO WORK!!!!!\n\n")
    ## Get gesture name from user to be used as button name
    gestName= str(input("Enter Gesture Name: "))
    ## Get auduio file name from the user
    fName= str(input("Enter Audio File Name with extension: "))
    ## Store these names in proper format in local dictionary
    addDict[gestName]= {}
    addDict[gestName]['fname']= fName
    addDict[gestName]['sync']= []
    ## Get timestamp and values of each motor from the user
    while True:
        clear()
        print("IMPORTANT NOTE: ENTER TIMES STAMPS SEQUENTIALLY FOR THE GESTURE TO WORK!!!!!\n\n")
        tStamp= int(input("Enter Time Stamp in ms: "))
        eb1= int(input("Left Eyebrow (10-99): "))
        eb2= int(input("Right Eyebrow (10-99): "))
        el1= int(input("Left Eyelid (10-99): "))
        el2= int(input("Right Eyelid (10-99): "))
        ey1= int(input("Left Eye Horizontal (10-99): "))
        ey2= int(input("Right Eye Horizontal (10-99): "))
        ey3= int(input("Left Eye Vertical (10-99): "))
        ey4= int(input("Right Eye Vertical (10-99): "))
        li1= int(input("Left Lip (10-99): "))
        li2= int(input("Right Lip (10-99): "))
        li3= int(input("Bottom Lip (10-99): "))
        ne1= int(input("Neck Horizontal (10-99): "))
        ne2= int(input("Neck Vertical (10-99): "))
        ## Ask the user if data entered for that timestamp is correct
        cData= int(input("Data Entered Correctly? \t1)Yes \t2)No: "))
        ## If correct, store in local library otherwise do not store it
        if cData == 2:
            continue
        ## If correct, store in local library otherwise do not store it
        addDict[gestName]['sync'].append({'time':tStamp,'eb1':eb1, 'eb2':eb2, 'el1':el1, 'el2':el2, 'ey1':ey1, 'ey2':ey2, 'ey3':ey3, 'ey4':ey4, 'li1':li1, 'li2':li2, 'li3':li3, 'ne1':ne1, 'ne2':ne2})
        ## Ask user if he wants to add more timestamps and values to this gesture to show different postures in different timestamp
        cnt= int(input("Enter \t1)More time Stamps. \t2)Done: "))
        ## If done, break the loop
        if cnt== 2:
            break
    ## Clear the screen
    clear()
    ## For final time, show all the values that is about to be written to the library file.
    print("Confirm the details of this gesture: ")
    ttl= list(addDict.keys())[0]
    print("Gesture Name: {}".format(ttl))
    print("Audio file name {}".format(addDict[ttl]['fname']))
    for dicts in addDict[ttl]['sync']:
        print("")
        for keys, values in dicts.items():
            print("{}: {}".format(keys, values))
    ## If all data entered is verified and correct, store the updated local dictionary to the library file otherwise do not use the data and erase it
    inp= int(input("1)Correct Info; \t2)Wrong Info: "))
    if inp== 1:
        clear()
        dictLoad.update(addDict)
        updateFile()
        print("Gesture Successfully Added")
    else:
        clear()
        print("Gesture Not Added")
    return


def main():
    while True:
        ## Main loop
        ## Show the menu to the user and ask the user for menu select option
        action= int(input("1)Add Gesture. \t2)Delete Gesture. \t3)List Gestures \t4)Exit Script \nEnter Number: "))
        if action== 4:
            ## Straightforward, exit the script
            break
        elif action== 3:
            ## Clear screen
            clear()
            ## load the library file
            loadLibrary()
            ## Display list of gestures
            displayAllGestures()
            ## User enter to contine
            _= input("Enter to Continue: ")
            ## Clear screen
            clear()
            continue
        elif action== 2:
            ## Clear screen
            clear()
            ## Load Library file
            loadLibrary()
            ## Display list of gestures present in library
            displayAllGestures()
            ## Delete user required gesture from the library file
            delGesture()
            ## Update the library file
            updateFile()
            time.sleep(5)
            clear()
            continue
        elif action== 1:
            ## Clear screen
            clear()
            ## Load Library file
            loadLibrary()
            ## Call add gesture function to add new user defined gesture
            addGesture()
            ## Clear screen once done successfully
            clear()
            print("Successful")
            time.sleep(4)
            clear()
            continue
        else:
            clear()
            ## If menu number entered out of bounds, let the user know and try again
            print("Enter valid number from the list")
            continue
    return



if __name__ == '__main__':
    ## Run main script only if this script running as main program
    main()
    ## Let user know if the program run successfully and exit the script
    print("Success!!!")
    time.sleep(1)