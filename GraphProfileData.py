import os
import lz4.block
import lz4.frame
import json
import statistics
import time
import re
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from scipy.stats import ttest_ind

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

colors = [
	'#e69f00',
	'#56b4e9',
	'#b4e956',
	# TODO: add more colors as necessary
]

builds = []
buildSet = set()

class DataPoint:
	def __init__(self, timeStamp, time, label):
		self.timeStamp = datetime.strptime(timeStamp[0:19], "%Y-%m-%dT%H:%M:%S")
		self.time = time
		self.label = label

# Creates DataPoint object from the json file. 
def addDataPoints(data, label):
	# Get the time stamp of this profile
	time = data['creationDate']

	# First paint measure
	firstPaint = data['payload']['simpleMeasurements']['firstPaint']
	firstPaintDataPoint = DataPoint(time, firstPaint, label)
	firstPaintList.append(firstPaintDataPoint)

	# About home top sites first paint
	aboutHomeFirstPaint = data['payload']['processes']['parent']['scalars']['timestamps.about_home_topsites_first_paint']
	firstPaintAboutHomeDataPoint = DataPoint(time, aboutHomeFirstPaint, label)
	firstPaintAboutHomeList.append(firstPaintAboutHomeDataPoint)

	readBytes = data['payload']['simpleMeasurements']['startupWindowVisibleReadBytes']
	readBytesDataPoint = DataPoint(time, readBytes, label)
	visibleReadBytes.append(readBytesDataPoint)

	isColdResults = data['payload']['processes']['parent']['scalars'].get('startup.is_cold', 0)
	isColdDataPoint = DataPoint(time, isColdResults, label)
	isCold.append(isColdDataPoint)


# Graphs the data from the given list. yAxis is an optional parameter that defaults to time.
def graphData(dataset, title, showHistogram, yAxis = "Time (ms)"):
	dataset.sort(key=lambda x: x.timeStamp, reverse=False)

	datasets = {}
	for build in builds:
		datasets[build['label']] = [x.time for x in dataset if x.label == build['label']]

	for build in builds:
		label = build['label']
		color = build['color']
		if len(datasets[label]) == 0:
			continue
		print("Mean for %s: %f" % (label, statistics.mean(datasets[label])))
		print("T-Test result: ")
		print(ttest_ind(datasets['control'], datasets[label]))

		plt.plot(
			[x.timeStamp for (i, x) in enumerate(dataset) if x.label == label],
			[x.time for x in dataset if x.label == label],
			'o',
			color = color,
			label = label)

	plt.legend()
	plt.show()

	if not showHistogram:
		return

	plt.hist([
			[x.time for x in dataset if x.label == build['label']] for build in builds
		], density = True,
		color = [build['color'] for build in builds],
		label = [build['label'] for build in builds],
		bins = 10)
	plt.legend()
	plt.show()


# Loop through all of the jsonlz4 files in folder
for filename in os.listdir(pathToExperimentFolder):
	if filename.endswith(".jsonlz4"):
		fileLocation = pathToExperimentFolder + '\\' + filename
		
		# See if it is a control or test build
		match = re.search(r"([a-z_]+)_[0-9]+", filename);
		buildLabel = match.group(1)
		if buildLabel not in buildSet:
			buildSet.add(buildLabel)
			buildColor = colors[len(builds)]
			builds.append({'label': buildLabel, 'color': buildColor})

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
			addDataPoints(data, buildLabel)

# Graph first paint
graphData(firstPaintList, "simpleMeasurements.firstPaint", True)

# Graph the about home top sites first paint
graphData(firstPaintAboutHomeList, "timestamps.about_home_topsites_first_paint", True)
