#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: zenobiojoao
"""

try:
    import vrep
    import datetime
    import time
    import json
except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

print('Program started')
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print('Connected to remote API server')

    leftMotorHandle = 0
    vLeft = 5
    rightMotorHandle = 0
    vRight = 5

    error, leftMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    if error != vrep.simx_return_ok:
        print(str(error) + '! ERROR: simxGetObjectHandle motor esquerdo')

    error, rightMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
    if error != vrep.simx_return_ok:
        print(str(error) + '! ERROR: simxGetObjectHandle motor direito')

    error = vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
    if error != vrep.simx_return_novalue_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity motor esquerdo')

    error = vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
    if error != vrep.simx_return_novalue_flag:
        print(str(error) + '! ERROR: simxSetJointTargetVelocity motor direito')

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_streaming)
    if error != vrep.simx_return_novalue_flag:
        print(str(error) + '! signalValue')
    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    data = vrep.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    date = str(datetime.datetime.now().time())
    date = date.replace(':', '_')
    date = date.replace('.', '_')

    dataList = []
    jsonList = []
    file = open("dados" + date + ".json", "w+")

    while vrep.simxGetConnectionId(clientID) != -1:
        error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
        data = vrep.simxUnpackFloats(signalValue)
        for i in range(int(len(data)/3)):
            if i+2 < len(data):
                dataDict = dict(x=data[i], y=data[i+1], z=data[i+2])
                dataList.append(dataDict)
        jsonList.append(dataList)
        time.sleep(1)

    jsonList = json.dumps(jsonList, indent=4, separators=(',', ': '))
    file.write(jsonList)
    file.close()

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)

else:
    print('Failed connecting to remote API server')
    print('Program ended')
