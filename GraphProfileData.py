import os
import lz4.block
import lz4.frame
import json
import time
import matplotlib.pyplot as plt
from pathlib import Path

home = str(Path.home())
pathToExperimentFolder = home + '\\Experiment'

# To add another graph:
# 1. Declare another list to hold data.
# 2. Append appropriate json info to list within 'addDataPoints'
# 3. Call graphData with list and appropriate title.

firstPaintList = []
firstPaintAboutHomeList = []
visibleReadBytes = []
isCold = []

class DataPoint:
	def __init__(self, timeStamp, time, isControl):
		self.timeStamp = timeStamp
		self.time = time
		self.isControl = isControl

# Creates DataPoint object from the json file. 
def addDataPoints(data, isControl):
	# Get the time stamp of this profile
	time = data['creationDate']

	# First paint measure
	firstPaint = data['payload']['simpleMeasurements']['firstPaint']
	firstPaintDataPoint = DataPoint(time, firstPaint, isControl)
	firstPaintList.append(firstPaintDataPoint)

	# About home top sites first paint
	aboutHomeFirstPaint = data['payload']['processes']['parent']['scalars']['timestamps.about_home_topsites_first_paint']
	firstPaintAboutHomeDataPoint = DataPoint(time, aboutHomeFirstPaint, isControl)
	firstPaintAboutHomeList.append(firstPaintAboutHomeDataPoint)

	readBytes = data['payload']['simpleMeasurements']['startupWindowVisibleReadBytes']
	readBytesDataPoint = DataPoint(time, readBytes, isControl)
	visibleReadBytes.append(readBytesDataPoint)

	isColdResults = data['payload']['processes']['parent']['scalars']['startup.is_cold']
	isColdDataPoint = DataPoint(time, isColdResults, isControl)
	isCold.append(isColdDataPoint)


# Graphs the data from the given list. yAxis is an optional parameter that defaults to time.
def graphData(list, title, yAxis = "Time (ms)"):
	list.sort(key=lambda x: x.timeStamp, reverse=False)
	for data in list:
		if data.isControl:
			plt.plot(data.timeStamp, data.time, 'bo')
		else:
			plt.plot(data.timeStamp, data.time, 'yo')
	plt.xlabel("Trial")
	plt.ylabel(yAxis)
	plt.title(title)
	plt.xticks(rotation=90)
	plt.tight_layout()
	plt.show()


# Loop through all of the jsonlz4 files in folder
for filename in os.listdir(pathToExperimentFolder):
	if filename.endswith(".jsonlz4"):
		fileLocation = pathToExperimentFolder + '\\' + filename
		
		# See if it is a control or test build
		isControl = False
		if 'control' in filename:
			isControl = True

		# Decompress files and convert to json
		bytestream = open(fileLocation, "rb")
		bytestream.read(8)
		valid_bytes = bytestream.read()
		text = lz4.block.decompress(valid_bytes)

		# Write data to new json files
		newFile = pathToExperimentFolder + '\\' + os.path.splitext(filename)[0] + '.json'

		with open(newFile, 'wb') as fin:
			fin.write(text)
		with open(newFile, 'r') as fin:
			data = json.load(fin)
			addDataPoints(data, isControl)

# Graph first paint
graphData(firstPaintList, "Time from first paint")

# Graph the about home top sites first paint
graphData(firstPaintAboutHomeList, "Time from first paint about home top sites")

# Graph the visible read bytes
graphData(visibleReadBytes, "Read bytes from startup", "Number of Bytes (mb)")