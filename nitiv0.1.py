import datetime
import pandas as pd
import numpy as np
import math

speedLimit = {'Delhi' : 50}		#Specifying speed limits in the areas to detect overspeeding
HarshAccThreshold = 1.5		# m / s ^ 2
HarshBrakThreshold = 1.8	# m / s ^ 2

HeartBeat = 5

MaxAllowedPositiveChange = HarshAccThreshold * HeartBeat * 18 / 5		#maximum allowed speed change in case of acceleration in a heartbeat for smooth driving
MaxAllowedNegativeChange = HarshBrakThreshold * HeartBeat * 18 / 5		#maximum allowed speed change in case of braking in a heartbeat for smooth driving


WarningExtraSpeed = 1.1
OverspeedRatingDecreaseParameter = 50
CollisionRatingDecreaseParameter = 150
AccRatingDecreaseParameter = 25
BrakRatingDecreaseParameter = 50
IdleRatingIncreaseParameter = 0.1

OneLatitude=111000	# Distance in one degree of latitude in metres
OneLongitude=87870	# Distance in one degree of longitude in metres


ratingData = pd.read_csv(r'H:\Book1.csv', index_col = False)
data = pd.read_csv(r'H:\YASH.csv', index_col = False)

timeNow = datetime.datetime(2018, 8, 26, 17, 13, 13)	# timestamp will be changed to required time at which the set of details is received, current time is just assumed here
strtimeNow = str(timeNow.isoformat())

TotalDevices = ratingData.shape[0]
TotalReadings = data.shape[0]

def IncreaseRating(DeviceCode):
	OwnDetailsFromRating = ratingData.loc[ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)])]	#getting own ratings
	OwnRatings = float(OwnDetailsFromRating['Ratings'])
	
	IncreaseRatio = 1 - (OwnRatings / 10000)
	NewRating = OwnRatings + (IdleRatingIncreaseParameter * IncreaseRatio)
	for index, row in ratingData.iterrows():
			if str(row['deviceCode_deviceCode']) == str(DeviceCode):
				ratingData['Ratings'][index] = str(NewRating)
	ratingData.to_csv(r'H:\1.csv')

def BrakingAndAcceleration(DeviceCode, CurrentDetails, VehiclePreviousStats, VehicleinArea):
	CurrentSpeed = int(CurrentDetails['deviceCode_pyld_speed'].values[0])
	PreviousSpeed = int(VehiclePreviousStats['deviceCode_pyld_speed'].values[0])
	SpeedDifference = CurrentSpeed - PreviousSpeed
	PastOwnLatitude = float(OwnVehiclePreviousStats['deviceCode_location_latitude'].values[0])
	PastOwnLongitude = float(OwnVehiclePreviousStats['deviceCode_location_longitude'].values[0])
	
	
	if PreviousSpeed < CurrentSpeed and MaxAllowedPositiveChange < SpeedDifference:
		
		OwnDetailsFromRating = ratingData.loc[ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)])]	#getting own ratings
		OwnRatings = float(OwnDetailsFromRating['Ratings'])
		
		NewRating = OwnRatings - (AccRatingDecreaseParameter * OwnRatings / 1000)
		
		for index, row in ratingData.iterrows():
			if str(row['deviceCode_deviceCode']) == str(DeviceCode):
				ratingData['Ratings'][index] = str(NewRating)
		
		
		ratingData.to_csv(r'H:\1.csv')
		
		print( "Harsh Acceleration")
		
	elif PreviousSpeed > CurrentSpeed and MaxAllowedNegativeChange < abs(SpeedDifference):
		CurrentLatitude = CurrentDetails['deviceCode_location_latitude']
		CurrentLongitude = CurrentDetails['deviceCode_location_longitude']
	
		aaaa = ratingData[0:0]
	
		for index, row in VehiclesInArea.iterrows():
			if (float(row['deviceCode_location_latitude']) - CurrentLatitude < 0.0001).all() & (float(row['deviceCode_location_longitude']) - CurrentLongitude < 0.00015).all()	:
				aaaa = aaaa.append(row)
	
		
		for index, row in aaaa.iterrows():
			CurrentSuspect = row
			DeviceID = CurrentSuspect['deviceCode_deviceCode']
			SuspectLatitude = CurrentSuspect['deviceCode_location_latitude']
			SuspectLongitude = CurrentSuspect['deviceCode_location_longitude']
			DistanceFound = CalculateDistanceDifference(CurrentLatitude, CurrentLongitude, SuspectLatitude, SuspectLongitude)
			print('\n\n\n',DistanceFound,'\n\n')
			if (DistanceFound < 10).all():
				LatitudeDif = PastOwnLatitude - CurrentLatitude
				LongitudeDif = PastOwnLongitude - CurrentLongitude
				if ((PastOwnLongitude - CurrentLongitude) > 0).all() and (CurrentLongitude > SuspectLatitude).all() and ((PastOwnLatitude - CurrentLatitude) > 0).all() and (CurrentLatitude > SuspectLatitude).all() :
					pass
				elif (((PastOwnLongitude - CurrentLongitude) > 0).all() and (CurrentLongitude > SuspectLatitude).all() and ((PastOwnLatitude - CurrentLatitude) < 0).all() and (CurrentLatitude < SuspectLatitude).all()) :
					pass
				elif ((PastOwnLongitude - CurrentLongitude) < 0).all() and (CurrentLongitude < SuspectLatitude).all() and ((PastOwnLatitude - CurrentLatitude) > 0).all() and (CurrentLatitude > SuspectLatitude).all() :
					pass
				elif ((PastOwnLongitude - CurrentLongitude) < 0).all() and (CurrentLongitude < SuspectLatitude).all() and ((PastOwnLatitude - CurrentLatitude) < 0).all() and (CurrentLatitude < SuspectLatitude).all() :
					pass
				else:
					OwnDetailsFromRating = ratingData.loc[ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)])]	#getting own ratings
					OwnRatings = float(OwnDetailsFromRating['Ratings'])
					print(OwnRatings)
					NewRating = float(OwnRatings) - (BrakRatingDecreaseParameter * float(OwnRatings) / 1000)
			
					for index, row in ratingData.iterrows():
						if str(row['deviceCode_deviceCode']) == str(DeviceCode):
							ratingData['Ratings'][index] = str(NewRating)
			
			
					ratingData.to_csv(r'H:\1.csv')
					
					print( 'Harsh Braking')
			else:
				OwnDetailsFromRating = ratingData.loc[ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)])]	#getting own ratings
				OwnRatings = OwnDetailsFromRating['Ratings']
				NewRating = float(OwnRatings) - (BrakRatingDecreaseParameter * float(OwnRatings) / 1000)
				for index, row in ratingData.iterrows():
					if str(row['deviceCode_deviceCode']) == str(DeviceCode):
						ratingData['Ratings'][index] = str(NewRating)
						
				ratingData.to_csv(r'H:\1.csv')
				print('Harsh Braking')
			
	else:
		return False
	

def OverspeedingCheck(DeviceCode, CurrentSpeed, SpeedLimit):
	WarningSpeed = SpeedLimit * WarningExtraSpeed		#1.1 is just for giving the warning till 10% extra speed, can be changed to 1.25 for 25% extra speed
	OwnDetails = ratingData.loc[(ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)]))]
	if int(CurrentSpeed) < SpeedLimit:
		return False
	
	elif int(CurrentSpeed) < WarningSpeed and int(CurrentSpeed) > SpeedLimit:
		print('Overspeeding Warning')
	
	elif int(CurrentSpeed) > WarningSpeed:
		OwnRatings = float(OwnDetails['Ratings'])
		SpeedRatio = CurrentSpeed / SpeedLimit
		DeductionRatio = SpeedRatio - 1
		NewRating = OwnRatings - ((OverspeedRatingDecreaseParameter * DeductionRatio) * OwnRatings / 1000)		#30 here is assumed to be adequate for decreasing the rating, if speeding is more important for good rating then it can be increased to 50 - 75
		'''
		The above statement is for the dynamic decrease in the ratings depending on the previous rating of the device.
		Higher the rating, more will be the decrease conpared to that with lower ratings
		'''
		
		for index, row in ratingData.iterrows():
			if str(row['deviceCode_deviceCode']) == str(DeviceCode):
				ratingData['Ratings'][index] = str(NewRating)
		
		
		ratingData.to_csv(r'H:\1.csv')

		print('Rating Decreased, OverSpeeding')
		
		
def UpdateRating(DeviceID):
	OwnDetails = ratingData.loc[(ratingData['deviceCode_deviceCode'].isin([str(DeviceCode)]))]	#getting own ratings
	SuspectDetails = ratingData.loc[(ratingData['deviceCode_deviceCode'].isin([str(DeviceID)]))]	#getting the ratings of the collided vehicle
	OwnRatings = OwnDetails['Ratings']
	SuspectRating = SuspectDetails['Ratings']
	
	NewRating = float(OwnRatings) - (float(CollisionRatingDecreaseParameter) * float(OwnRatings) / 1000)
	for index, row in ratingData.iterrows():
		if str(row['deviceCode_deviceCode']) == str(DeviceCode):
			ratingData['Ratings'][index] = str(NewRating)
	
	ratingData.to_csv(r'H:\1.csv')
	
	
	print('Ratings Updates due to Collision')
	

def CollisionAlarm(DeviceApproaching_ID):
	'''
	Finding the distance between the suspected vehicle in previous updated stats so that we can find whether the vehicle is getting closer or far
	'''
	
	previousStatTime = (timeNow - datetime.timedelta(0,HeartBeat)).isoformat() # HeartBeat is the time interval of updation of the database with new information in seconds
	SuspectedVehicleCurrentStats = data.loc[(data['deviceCode_deviceCode'].isin([DeviceApproaching_ID])) & (data['deviceCode_time_recordedTime_$date'].isin([str(strtimeNow)]))]
	SuspectedVehiclePreviousStats = data.loc[(data['deviceCode_deviceCode'].isin([DeviceApproaching_ID])) & (data['deviceCode_time_recordedTime_$date'].isin(([str(previousStatTime)])))]
	OwnVehicleCurrentStats = data.loc[(data['deviceCode_deviceCode'].isin([DeviceCode])) & (data['deviceCode_time_recordedTime_$date'].isin(([str(strtimeNow)])))]
	OwnVehiclePreviousStats = data.loc[(data['deviceCode_deviceCode'].isin([DeviceCode])) & (data['deviceCode_time_recordedTime_$date'].isin([str(previousStatTime)]))]
	PastOwnLatitude = float(OwnVehiclePreviousStats['deviceCode_location_latitude'].values[0])
	PastOwnLongitude = float(OwnVehiclePreviousStats['deviceCode_location_longitude'].values[0])
	PastSuspectLatitude = float(SuspectedVehiclePreviousStats['deviceCode_location_latitude'].values[0])
	PastSuspectLongitude = float(SuspectedVehiclePreviousStats['deviceCode_location_longitude'].values[0])
	
	PreviousDistance = CalculateDistanceDifference(PastOwnLatitude, PastOwnLongitude, PastSuspectLatitude, PastSuspectLongitude)
	
	CurrentOwnLatitude = float(OwnVehicleCurrentStats['deviceCode_location_latitude'])
	CurrentOwnLongitude = float(OwnVehicleCurrentStats['deviceCode_location_longitude'])
	CurrentSuspectLatitude = float(SuspectedVehicleCurrentStats['deviceCode_location_latitude'])
	CurrentSuspectLongitude = float(SuspectedVehicleCurrentStats['deviceCode_location_longitude'])
	
	CurrentDistance = CalculateDistanceDifference(CurrentOwnLatitude, CurrentOwnLongitude, CurrentSuspectLatitude, CurrentSuspectLongitude)
	
	DistanceDifference = CurrentDistance - PreviousDistance
	
	if PreviousDistance < CurrentDistance:
		return False
	
	elif PreviousDistance > CurrentDistance and CurrentDistance < 50:
		CurrentOwnSpeed = OwnVehicleCurrentStats['deviceCode_pyld_speed']
		CurrentOwnSpeed = CurrentOwnSpeed * 1000 / 3600		#converting speed to m / s so that all units remain same
		CurrentSuspectSpeed = SuspectedVehicleCurrentStats['deviceCode_pyld_speed']
		CurrentSuspectSpeed = CurrentSuspectSpeed * 1000 / 3600		#converting speed to m / s so that all units remain same
		SpeedTotal = CurrentOwnSpeed + CurrentSuspectSpeed
		SpeedApproach = DistanceDifference / HeartBeat
		if CurrentOwnLatitude < CurrentSuspectLatitude and CurrentOwnLongitude == CurrentSuspectLongitude and CurrentDistance > 3:
			print( DeviceCode,'Vehicle Approaching from North')
			return False
		elif CurrentOwnLatitude > CurrentSuspectLatitude and CurrentOwnLongitude == CurrentSuspectLongitude and CurrentDistance > 3:
			print( DeviceCode, 'Vehicle Approaching from South')
			return False
		elif CurrentOwnLatitude == CurrentSuspectLatitude and CurrentOwnLongitude < CurrentSuspectLongitude and CurrentDistance > 3:
			print(  DeviceCode,'Vehicle Approaching from East')
			return False
		elif CurrentOwnLatitude == CurrentSuspectLatitude and CurrentOwnLongitude > CurrentSuspectLongitude and CurrentDistance > 3:
			print( DeviceCode, 'Vehicle Approaching from West')
			return False
		elif CurrentOwnLatitude < CurrentSuspectLatitude and CurrentOwnLongitude < CurrentSuspectLongitude and CurrentDistance > 3:
			print(  DeviceCode,'Vehicle Approaching from North-East')
			return False
		elif CurrentOwnLatitude < CurrentSuspectLatitude and CurrentOwnLongitude > CurrentSuspectLongitude and CurrentDistance > 3:
			print(  DeviceCode,'Vehicle Approaching from North-West')
			return False
		elif CurrentOwnLatitude > CurrentSuspectLatitude and CurrentOwnLongitude < CurrentSuspectLongitude and CurrentDistance > 3:
			print(  DeviceCode,'Vehicle Approaching from South-East')
			return False
		elif CurrentOwnLatitude > CurrentSuspectLatitude and CurrentOwnLongitude > CurrentSuspectLongitude and CurrentDistance > 3:
			print(  DeviceCode,'Vehicle Approaching from South-West')				
			return False
		elif SpeedApproach >= 10:
			print('Medical Attention Needed')			#assuming if the accident is happened at the combined speed > 10 m / s i.e. 36 km / hr
		elif SpeedApproach < 10:
			print('Inform Traffic Department')
		'''
		The above statements checks the speed by which the vehicles collided and depending on the speed of collision, whether medical attention is needed or not
			'''
	
def CalculateDistanceDifference(LatitudeSelf,LongitudeSelf,Latitude,Longitude): #Calculate Distance between two locations
	LatDifference = LatitudeSelf - Latitude
	LatDistance = LatDifference * OneLatitude
	LongDifference = LongitudeSelf - Longitude
	LongDistance = LongDifference * OneLongitude
	SeperateDistance = (LatDistance ** 2 + LongDistance ** 2) ** 0.5
	return SeperateDistance

	
for i in range(0, TotalReadings // TotalDevices-1):	

	for i in range(0 , TotalDevices):
		DeviceCode = str(ratingData.iloc[i]['deviceCode_deviceCode']) #Own Device ID fitted in vehicle
		CurrentDetails = data[(data['deviceCode_deviceCode'].isin([str(DeviceCode)])) & (data['deviceCode_time_recordedTime_$date'].isin([str(strtimeNow)]))]
		print(DeviceCode,CurrentDetails)
		CurrentLatitude = float(CurrentDetails['deviceCode_location_latitude'].values[0])
		CurrentLongitude = float(CurrentDetails['deviceCode_location_longitude'].values[0])

		LocationOfVehicle = (CurrentDetails['deviceCode_location_wardName'])

		LocationOfVehicle = LocationOfVehicle.values[0]

		SpeedLimit = speedLimit[LocationOfVehicle]
		SpeedVehicle = CurrentDetails['deviceCode_pyld_speed'].values[0]
		OverVar = OverspeedingCheck(DeviceCode, SpeedVehicle, SpeedLimit)	

		previousStatTime = (timeNow - datetime.timedelta(0, HeartBeat)).isoformat() # UpdateTimeSpan is the time interval of updation of the database with new information in seconds
		OwnVehiclePreviousStats = data.loc[(data['deviceCode_deviceCode'].isin([str(DeviceCode)])) & (data['deviceCode_time_recordedTime_$date'].isin([str(previousStatTime)]))]
		aaaa = data[(data['deviceCode_time_recordedTime_$date'].isin([str(strtimeNow)])) & ~(data['deviceCode_deviceCode'].isin([str(DeviceCode)]))]
		
		VehiclesInArea = CurrentDetails
		VehiclesInArea = VehiclesInArea.iloc[0:0]
		
		for index, row in aaaa.iterrows():
			if (float(row['deviceCode_location_latitude']) - CurrentLatitude < 0.0008) & (float(row['deviceCode_location_longitude']) - CurrentLongitude < 0.0009):
				VehiclesInArea = VehiclesInArea.append(row)
		
		NumberVehicleInArea = VehiclesInArea.shape[0]

		CollisionFlag = 1

		for index, row in VehiclesInArea.iterrows():
			CurrentSuspect = row
			DeviceID = CurrentSuspect['deviceCode_deviceCode']
			SuspectLatitude = CurrentSuspect['deviceCode_location_latitude']
			SuspectLongitude = CurrentSuspect['deviceCode_location_longitude']
			DistanceFound = CalculateDistanceDifference(CurrentLatitude, CurrentLongitude, SuspectLatitude, SuspectLongitude)
			if DistanceFound >= 3:		#assuming that 3 m is the max safe distance can be adjust depending on the size of vehicle
				CollisionAlarm(DeviceID)

			else:
				print(DeviceCode, "Alert: Collision Detected.")
				UpdateRating(DeviceCode)
				CollisionFlag = 0

					
		BrakingAndAccelerationResult = BrakingAndAcceleration(DeviceCode, CurrentDetails, OwnVehiclePreviousStats, VehiclesInArea)
		
		if not BrakingAndAccelerationResult and (OverVar == False) and CollisionFlag == 1:
			IncreaseRating(DeviceCode)
			print('Increased')
		
		
	timeNow = timeNow + datetime.timedelta(0,HeartBeat)
	strtimeNow = (timeNow.isoformat())