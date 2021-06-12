## import all required libraries
import csv
import numpy as np
import json
import os
import time
import sys

## variables to store all all required data in a list format
a= []
b= []
c= []
## Variables to store minimum and maximum values of required landmark points
maxes= []
mins= []

## Current Directory
cDir= os.getcwd()

## Get x, y coordinates of each landmark for all 90 timestamps.
def getAllPoints():
    global a
    ## Get csv file name which is to be used and processed
    fl= input("Enter File Name: ")
    try:
        ## Load the file and write the values to the variable to be processed in other functions
        with open(cDir + "/csvFiles/" + fl, mode='r') as employee_file:
            for line in csv.reader(employee_file):
                if line:
                    try:
                        a[int(line[0])].append(line[1:3])
                        pass
                    except:
                        a.insert(int(line[0]), [line[1:3]])
    except:
        ## If entered file is not found in the directory, notify the user and exit.
        print("File Not Found. Please confirm name and try again with extension.")
        time.sleep(5)
        sys.exit(1)


## This function get only required points from all the set of points. 
def getReqPoints():
    global a
    global b
    for i in range(0,91):
        ## Take required points and also process the data to have single values for each required landmarks and DOF parts
        b.insert(i, [int(a[i][19][1]),  int(a[i][25][1]), int(a[i][37][1]) - int(a[i][40][1]), int(a[i][44][1]) - int(a[i][47][1]), int(a[i][51][1]) - int(a[i][48][1]), int(a[i][51][1]) - int(a[i][54][1]), int(a[i][51][1]) - int(a[i][58][1])])
    pass

## Normalize the required landmarks according the 1st time stamp coordinates of all the required points processed.
def normalize():
    global a,b,c
    for i in range(1,90):
        for j in range(0,7):
            ## Normalizing all timestamps in accordance with 1st time stamp
            b[i][j]= int(b[0][j]) - int(b[i][j])
    for i in range(0,7):
        b[0][i]= 0
    pass


## Get maximum and minimum values that a each required landmark has reached
def getMaxes():
    global a,b,c, maxes, mins
    arr= []
    for i in range(0, 7):
        arr.clear()
        for j in range(0, 90):
            arr.append(int(b[j][i]))
        ## Get these values and append to another list to use it later
        maxes.append(max(arr))
        mins.append(min(arr))

##  This function simply maps the maximum value and the corrent value to its corresponding 100% value and returns required mapped value
def mapper(val, maxVal, maxCorr):
    return int((val*maxCorr)/maxVal)

## Process the data to required % values.
def TOtStampArr():
    global a,b,c,maxes,mins
    for i in range(0, 90):
        #eb1
        ## Process Left Eyebrow landmarks for all timestamp
        if b[i][0] < 0:
            t1= 50 - mapper(abs(b[i][0]), abs(mins[0]), 50)
        else:
            t1= 50 + mapper(abs(b[i][0]), abs(maxes[0]), 50)

        #eb2
        ## Process Right Eyebrow landmarks for all timestamp
        if b[i][1] < 0:
            t2= 50 - mapper(abs(b[i][1]), abs(mins[1]), 50)
        else:
            t2= 50 + mapper(abs(b[i][1]), abs(maxes[1]), 50)

        #el1
        ## Process Left Eyelid landmarks for all timestamp
        if b[i][2] < 0:
            t3= 50 + mapper(abs(b[i][2]), abs(mins[2]), 50)
        else:
            t3= 50 - mapper(abs(b[i][2]), abs(maxes[2]), 50)

        #el2 
        ## Process Right Eyelid landmarks for all timestamp
        if b[i][3] < 0:
            t4= 50 + mapper(abs(b[i][3]), abs(mins[3]), 50)
        else:
            t4= 50 - mapper(abs(b[i][3]), abs(maxes[3]), 50)

        #l1
        ## Process Left Lip landmarks for all timestamp
        if b[i][4] < 0:
            t5= 50 - mapper(abs(b[i][4]), abs(mins[4]), 50)
        else:
            t5= 50 + mapper(abs(b[i][4]), abs(maxes[4]), 50)

        #l2
        ## Process Right Lip landmarks for all timestamp
        if b[i][5] < 0:
            t6= 50 - mapper(abs(b[i][5]), abs(mins[5]), 50)
        else:
            t6= 50 + mapper(abs(b[i][5]), abs(maxes[5]), 50)

        #l3
        ## Process Bottom Lip landmarks for all timestamp
        if b[i][6] < 0:
            t7= 50 - mapper(abs(b[i][6]), abs(mins[6]), 50)
        else:
            t7= 50 + mapper(abs(b[i][6]), abs(maxes[6]), 50)


        ## Write all processed data to final array that is to be written and stored in library file
        try:
            c[i].append([abs(t1), abs(t2), abs(t3), abs(t4), abs(t5), abs(t6), abs(t7)])
            pass
        except:
            c.insert(i, [abs(t1), abs(t2), abs(t3), abs(t4), abs(t5), abs(t6), abs(t7)])
    pass

## Write the processed data to library file
def updateLib():
    ## get audio file name
    audioName= input("Enter audio file name: ")

    ## get btn name
    btnName= input("Enter Button Name: ")

    ## Read current contents of library file
    with open(cDir + '/library.json') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    js = json.loads(data)

    ## append btn name, file name, time-stampss along with motor movements,
    js[btnName]= {}
    js[btnName]["fname"]= audioName
    js[btnName]["sync"]= []
    for i in range(0,90):
        ## Write all processed data to properly timed stamps in json format
        js[btnName]["sync"].append({"time": i*167, "eb1": c[i][0], "eb2": c[i][1], "el1": c[i][2], "el2": c[i][3], "li1": c[i][4], "li2": c[i][5], "li3": c[i][6]})
    
    ## write entire library to file and save.
    with open('{}/library.json'.format(cDir), 'w') as fp:
        json.dump(js, fp)
    pass


if __name__ == '__main__':
    ## Run this script only if running as main
    ## First get all points from csv file
    getAllPoints()
    ## Get only required landmarks from this heap
    getReqPoints()
    ## Normalize all these points according to 1st x, y coordinate timestamps
    normalize()
    ## Get minimum and maximum value that the required points have reached
    getMaxes()
    ## Process all landmarks and convert to values between 10-100% according to the min and max values reached
    TOtStampArr()
    ## Write the final processed data to the library file
    updateLib()
    ## Notify the user all data successfully processed and written
    print("Success!!!")
    time.sleep(5)