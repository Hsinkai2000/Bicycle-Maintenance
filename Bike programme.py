#from sense_hat import SenseHat
from datetime import datetime
import time
#sense = SenseHat()
today = datetime.now()
#definitions
bicyclelist = []
option6list =["Pitch","Roll","Yaw","Movement","Temp","Batt %","KM"]
#read bike info
def readbikeinfo1():
    lines = 0
    #prompt
    filename = str(input("Enter the name of the data file :"))
    #open file
    with open(filename,'r') as file:
            #count lines
            for line in file:
                    lines += 1
                    line = line.strip()
                    #remove \n
                    bicyclelist.append(line.split(','))

            #minus heading line
            lines = lines - 1

    return lines

#display bikes info 
def displayallbikeinfo2(listofbikes, today):
    repairlist = []
    reasonlist = []
    #count num days
    for index in range (1, len(listofbikes)):
            newlist = []
            maintime = listofbikes[index][3]
            maintime = datetime.strptime(maintime, '%d/%m/%Y')
            differencetime = today - maintime
            #check and append reason to reasonlist and add Y/N
            if int(differencetime.days) >= 180 or float(listofbikes[index][4]) >= 50 or int(listofbikes[index][2]) < 10:
                    repairlist.append("Y")
                    if int(differencetime.days) >= 180:
                            newlist.append('months')
                    if float(listofbikes[index][4]) >= 50:
                            newlist.append('km')
                    if int(listofbikes[index][2]) < 10:
                            newlist.append('battery')
                    
            else:
                    repairlist.append("N")
                    #add empty list if N
                    newlist = []
            reasonlist.append(newlist)
            #insert & if needed
            for reasons in reasonlist:
                    if len(reasons) > 1:
                            reasons.insert(-1,'&')
    return repairlist, reasonlist
                    
#display selected bike info
def disbike3():
    newlist = []
    proceed = True
    #open file
    file = open('Assignment_Data2.csv','r')
    #add to list
    for item in file:
            newlist.append(item.split(','))
    #remove \n
    for thing in range(len(newlist)):
            newlist[thing][-1] = newlist[thing][-1].strip()
    while proceed:
            #prompt till available bike selected
            bikenum = input("Enter a bike no. : ")
            print()
            for bike in newlist:
                    if bikenum == bike[0]:
                            proceed = False
                
    return newlist, bikenum
            
#adding a bike
def addbike4(day):
    #default list with constants
    defaultlist = ['','','100','','0.00']
    day = day.strftime("%d/%m/%Y")
    #open file 
    with open('Assignment_Data1.csv', 'a') as file:
            
            #prompt 
            bikeno = input("Bike no. : " )
            date = input("Purchase date dd/mm/yyyy : ")
            #add to default list
            defaultlist[0] = defaultlist[0]+bikeno
            defaultlist[1] = defaultlist[1]+date
            defaultlist[3] = defaultlist[3]+str(day)
            #append to csv
            for i,item in enumerate(defaultlist):
                    if i == 4:
                            #next line if last item
                            file.write(item+'\n')
                    else:   
                            #else next square
                            file.write(item+',')
    #add new bike to bicyclelist 
    bicyclelist.append(defaultlist)
    print()
    print("Bicycle ({}) has been created.".format(bikeno))
    

#maintenance
def bikemaintenance5(reason, listofbikes):
    needmaintenance = []
    #check which bike needs maintenance & find reason
    for check in range(len(reason)):
            if reason[check] != []:
                    needmaintenance.append(check)
    return needmaintenance

#ridebike6
def ridebike6(listofbikes,repairlist):
    
    availablebike = []
    #check which bike can be ridden
    for i,item in enumerate(repairlist):
            if item == 'N':
                    availablebike.append(listofbikes[i+1])
    return availablebike

'''def getinfo(battery):   
    #have a dist counter
    distcounter = 0
    #timecounter
    t = 0
    #run fr 15sec (5 times with 3sec intervals + 1 starting)
    while t<6:
            #clear existing lights
            sense.clear
            
            #get temp & 1dp
            temp = sense.get_temperature()
            temp = round(temp,1)           
            
            #get charging temp & 1dp
            tempcharging = int(temp) + 0.5
            tempcharging = round(tempcharging,1)
            
            #get orientation
            o = sense.get_orientation()           
            pitch = o["pitch"]
            roll = o["roll"]
            yaw = o["yaw"]
            
            #round number for orientation
            pitch = round(pitch)
            roll = round(roll)
            yaw = round(yaw)
            
            #set as new orientation 
            currentorientation = [pitch, roll, yaw]
            
            if t == 0:
                    #print info
                    print("pitch: {}; roll: {}; yaw: {}; temp: {}".format(pitch, roll, yaw,temp))
                    print()

                    for heading in option6list:
                            print("{:<10}".format(heading))
                    print("\n")
                    print("-"*40)
                    
                    #set orientation as old
                    oldorientation = currentorientation#loop 1
            else:   
                    #find overall change in direction
                    a = abs((currentorientation[0] - oldorientation[0]))\
                    + abs((currentorientation[1] - oldorientation[1]))\
                    + abs((currentorientation[2] - oldorientation[2]))
                    
                    #get new temp
                    newtemp = sense.get_temperature()
                    newtemp = round(newtemp,1)
                    
                    #check if moved
                    if a > 20:
                            movement = "True"
                            #check temp > charging
                            if newtemp > tempcharging:
                                    battery += 1
                                    distcounter += 0.01
                    else:
                            movement = "False"
                            battery -= 1
                    print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".\
                    format(pitch, roll, yaw, movement, newtemp, battery, distcounter))               
                    oldorientation = currentorientation
                    
            #show batt 
            o = (1,1,1)
            x = (255,0,0)
            g = (100, 150, 102)
            lights = [o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,
                    o,o,o,o,o,o,o,o,]
            #if even number
            if int(battery)%2 == 0:
                    num = int(battery)/2
                    for i in range(0,int(num)):
                            lights[i] = x
            #if odd number
            else:
                    num = (int(battery)-1)/2
                    for i in range(0,int(num)):
                            lights[i] = x
                    lights[int(num)] = g
            sense.set_pixels(lights)
            t += 1
            
            #wait 3sec
            time.sleep(3)
            
    secondscount = t*3
    print("Trip ended")
    print("You travelled {}km over {}seconds.".format(distcounter, secondscount))
    print("Thanks you for riding with oRide! :D")


    return distcounter, battery, secondscount '''
#actual thing		
def menu():
    print("ADMIN MENU \n===========")
    menulist = ["[1] Read bicycle info from file",
            "[2] Display all bicycle info with servicing indication",
            "[3] Display selected bicycle info",
            "[4] Add a bicycle",
            "[5] Perform bicycle maintenance"]
    for item in menulist:
            print(item)
    print()
    print("RIDER MENU \n===========")
    print("[6] Ride a bicycle \n \n[0] Exit")


    
while True:
    menu()	
    selection = int ( input("Enter your option : ") )
    if selection == 1:
            print("Option 1 : Read bicycle info from file\n")
            lines = readbikeinfo1()
            print("Number of bicycles records read:",lines)
            print()
                    
    elif selection == 2:
            i = 0
            today = datetime.now()
            print("Option 2: Display all bicycle info with servicing indication\n")
            #print headings
            repairlist = displayallbikeinfo2(bicyclelist, today)[0]
            for heading in bicyclelist[0]:
                    print("{:<18}".format(heading), end = '')
            print("Service?")
            print("{:<18}".format("-"*16)*6)
            for itemindex in range(1,len(bicyclelist)):
                    for info in range(0,5):
                            print("{:<18}".format(bicyclelist[itemindex][info]), end = '')
                    #print Y?N
                    print("{:<18}".format(repairlist[i]))
                    i +=1
            print()	
                    
    elif selection == 3:
            print("Option 3: Display selected bicycle info\n")
            theList, bicyclenum = disbike3()
            #print headings
            for heading in theList[0]:
                    print("{:<18}".format(heading), end = '')
            print()
            print("{:<18}".format("-"*14)*4)
            #print bike info
            for rideindex in range(1,len(theList)):
                    if theList[rideindex][0] == bicyclenum:
                            for i,info in enumerate(theList[rideindex]):
                                    #add km,sec if needed
                                    if i == 0 or i == 3:
                                            x = ''
                                    elif i == 1:
                                            x = 'sec'
                                    else:
                                            x = 'km'                                   
                                    print("{:<18}".format(info+x),end = '')
                            print()

            print()

    elif selection == 4:
            print("Option 4: Add a bicycle")
            print()
            addbike4(today)
            print()
                            
    elif selection == 5:
            a = 1
            c = 0
            whymaintain = displayallbikeinfo2(bicyclelist, today)[1]
            maintenancebike = bikemaintenance5(whymaintain, bicyclelist)
            print("Option 5: Perform bicycle maintenance\n")
            
            #print heading
            for i, heading in enumerate(bicyclelist[0]):
                    if i != 1:
                            print("{:<18}".format(heading), end = '')
            print("{:<18}".format("Reason/s"))
            print("{:<18}".format("-"*16)*5)
            
            #print maintenance bikes
            for indexes in maintenancebike:
                    for bikedata in bicyclelist[indexes+1]:
                            if bikedata != bicyclelist[indexes+1][1]:
                                    print("{:<18}".format(bikedata),end = '')
                    for item in whymaintain[indexes]:
                            print(item, end = ' ')

                    print()
                    
            #ask for input until available bike
            while True:
                    bike = input("Bike No.:")
                    for bicycle in range(len(bicyclelist)):
                            if bicyclelist[bicycle][0] != bike:
                                   continue
                            else:#if inside bicyclelist
                                    #if there is a reason (need maintenance)
                                    if whymaintain[bicycle-1] != []:
                                            c = 2
                                            actualindex = bicycle 
                                    else:
                                            c = 1

                            break
                    if c == 0:
                            print("No such bike!")
                                    
                    elif c == 1:
                            print("Bike not due for servicing!")           
                    elif c == 2:
                            #change data in bicyclelist
                            today = today.strftime("%d/%m/%Y")
                            bicyclelist[actualindex][3] = str(today)
                            bicyclelist[actualindex][2] = '100'
                            bicyclelist[actualindex][4] = '0'
                            #rewrite data in .csv
                            with open('Assignment_Data1.csv', 'w') as file:
                                    for listlist in bicyclelist:
                                            for i, itemtype in enumerate(listlist):
                                                    if i != 4:
                                                            file.write(itemtype+',')
                                                    if i == 4:
                                                            file.write(itemtype+'\n')                            
                            print('Bicycle serviced.')
                            break
                            
            #print remaining bike for servicing
            for i, heading in enumerate(bicyclelist[0]):
                    if i != 1:
                            print("{:<18}".format(heading), end = '')
            print("{:<18}".format("Reason/s"))
            print("{:<18}".format("-"*16)*5)
            
            #print maintenance bikes
            for indexes in maintenancebike:
                    if bicyclelist[indexes+1][0] != bike:
                            for bikedata in bicyclelist[indexes+1]:
                                    if bikedata != bicyclelist[indexes+1][1]:
                                            print("{:<18}".format(bikedata),end = '')
                            for item in whymaintain[indexes]:
                                    print(item, end = ' ')

                            print()
            
            
    elif selection == 6:
            a = 0
            print("Option 6: Ride a bicycle")
            print()
            #pring heading
            for i,heading in enumerate(bicyclelist[0]):
                    if i != 1 and i != 3:
                            print("{:<18}".format(heading),end = '')
            print()
            print("{:<18}".format("-"*16)*3)
            #print available bike
            bikelist = ridebike6(bicyclelist, repairlist)
            for bike in bikelist:
                    for i,info in enumerate(bike):
                            if i != 1 and i != 3 and i != 5:
                                    print("{:<18}".format(info),end = '')
                    print()
            #ask for input until available bike
            while True:
                    bike = input("Bike No.:")
                    for item in bikelist:
                            if item[0] != bike:
                                    continue 
                            elif item[0] == bike:
                                    a += 1
                    if a == 0:
                            print("No such bicycle")
                    else:
                            print("Riding bike no. {}...".format(bike))
                            for indexnum in range (len(bikelist)):
                                    if bike in bikelist[indexnum]:
                                            #take index of selected bike 
                                            wantnum = indexnum
                            #give battery % to function
                            bat = bikelist[wantnum][2]
                            break
            #getinfo(bat)
            distance, battery, secondscounter = getinfo(bat)
            endlist = [bikelist[wantnum][0], secondscounter, distance, battery]
            with open('Assignment_Data2.csv','a') as file:
                    for data in endlist:
                            file.write(str(data) + ',')
                            
    if selection == 0:
            break
