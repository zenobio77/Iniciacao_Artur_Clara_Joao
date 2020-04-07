#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019

@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes

"""

import time
import plotly.express as px
import pandas as pd
import datetime
from sklearn.cluster import DBSCAN

try:
    import vrep
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

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_streaming)
    if error == vrep.simx_return_remote_error_flag:
        print(str(error) + '! signalValue_streaming')
    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    if error == vrep.simx_return_novalue_flag:
        print(str(error) + '! signalValue_buffer')
    data = vrep.simxUnpackFloats(signalValue)
    time.sleep(0.1)

    dataComplete = []
    counter = 0
    while vrep.simxGetConnectionId(clientID) != -1:
        error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
        if error == vrep.simx_return_novalue_flag:
            print(str(error) + '! signalValue_buffer')
        data = vrep.simxUnpackFloats(signalValue)
        dataList = []
        for i in range(0, int(len(data)), 3):
            dataList.append(data[i+1])
        if len(dataList) != 0:
            dataComplete.append(dataList)
            counter += 1
        time.sleep(2)

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    vrep.simxFinish(clientID)

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    now = str(year) + "_" + str(month) + "_" + str(day) + "_" + str(hour) + "_" + str(minute) + "_" + str(second)

    pointList = []
    readingList = []
    valueList = []
    for i in range(len(dataComplete[len(dataComplete) - 1])):
        for j in range(len(dataComplete)):
            pointList.append(i)
            readingList.append(j)
            valueList.append(dataComplete[j][i])
    df = pd.DataFrame()
    df["point"] = pointList
    df["reading"] = readingList
    df["values"] = valueList
    df["label"] = [0] * len(df)

    for i in range(len(set(df["reading"]))):
        dfSingleReading = df.where(df["reading"] == i).dropna()
        dfSingleReading.drop(columns=["point", "reading"], inplace=True)
        db = DBSCAN(eps=0.5, min_samples=5).fit(dfSingleReading)
        dfSingleReading["label"] = db.labels_
        for index in list(dfSingleReading.index.values):
            df.loc[index, "label"] = dfSingleReading.loc[index, 'label']

    fig = px.scatter(df, y='values', color='label', animation_frame="reading", animation_group="point")
    fig.show()

    df.to_csv('data_' + now + ".csv")

else:
    print('Failed connecting to remote API server')
    print('Program ended')
