
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:47:12 2019
@author: João Gabriel Fernandes Zenóbio and Clara Loris de Sales Gomes
"""

try:
	import sim
	import time
	import pandas as pd
	import math
except ModuleNotFoundError:
	print("--------------------------------------------------------------")
	print("'sim.py' could not be imported. This means very probably that")
	print("either 'sim.py' or the remoteApi library could not be found.")
	print("Make sure both are in the same folder as this file,")
	print("or appropriately adjust the file 'sim.py'")
	print("--------------------------------------------------------------")
	print("")


class Pioneer:

	simxOpmodeStreamingToBuffer_FLAG = 0


	def set_position(self, x=-6.5, y=-12, z=0.3):
		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

		error = sim.simxSetObjectPosition(self.clientId, self.pioneerHandle, -1, (x, y, z), sim.simx_opmode_oneshot_wait)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetObjectPosition pioneer')

		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

	def get_position(self):
		error, position = sim.simxGetObjectPosition(self.clientId, self.pioneerHandle, -1, sim.simx_opmode_buffer)
		if error == sim.simx_return_novalue_flag:
				print(str(error) + "! simxGetObjectPosition_buffer")
		return position

	def set_orientation(self, a=0, b=0, g=90):
		a = math.radians(a)
		b = math.radians(b)
		g = math.radians(g)
		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error == sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')

		error = sim.simxSetObjectOrientation(self.clientId, self.pioneerHandle, -1, (a, b, g), sim.simx_opmode_oneshot_wait)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetObjectPosition pioneer')
		time.sleep(0.1)

		error = sim.simxSetModelProperty(self.clientId, self.pioneerHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty pioneer')
		error = sim.simxSetModelProperty(self.clientId, self.leftMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.leftMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.rightMotorHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.rightMotorHandle')
		error = sim.simxSetModelProperty(self.clientId, self.casterFreeHandle, not sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
		if error != sim.simx_return_ok:
			print(str(error) + '! ERROR: simxSetModelProperty self.casterFreeHandle')


	def get_laser_2d_data(self):
		error, signalValue = sim.simxGetStringSignal(self.clientId, "measuredDataAtThisTime", sim.simx_opmode_buffer)
		if error == sim.simx_return_novalue_flag:
			print(str(error) + "! signalValue_buffer")
		data = sim.simxUnpackFloats(signalValue)
		dataList = []
		for i in range(0, int(len(data)), 3):
			dataList.append(data[i+1])
		if len(dataList) == 182:
			time.sleep(0.1)
			return dataList
		else:
			return False
