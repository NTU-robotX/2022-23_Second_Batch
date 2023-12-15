# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time


def heartbeat():
    # Use a breakpoint in the code line below to debug your script.
    msgDate = time.strftime("%d%m%y")  # following RobotX 2023 format ddmmyy
    msgTime = time.strftime("%H%M%S")  # following RobotX 2023 format hhmmss
    msgLat = '21.31198'  # Current Latitude in Decimal degrees
    msgNS = 'N'  # N-North, S-South
    msgLon = '157.88972'  # Current Longitude in Decimal degrees
    msgEW = 'W'  # East/West
    msgTeamID = 'SINGABOAT'
    msgSysMode = '2'  # 1- remote op 2 - autonomous 3- killed
    msgUAVStat = '1'  # 1-stowed 2-deploy 3-fault
    print('$RXHRB,%s,%s,%s,%s,%s,%s,%s,%s,%s*11' % (
        msgDate, msgTime, msgLat, msgNS, msgLon, msgEW, msgTeamID, msgSysMode, msgUAVStat))
    return
    # print('$RXHRB,%s,%s,LAT,N,LON,W,SINGABOAT,' % (time.strftime("%d%m%y"),
    #                          time.strftime("%H%M%S"))) # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.

heartbeat()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
