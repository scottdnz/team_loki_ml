import os
import json
import csv
from datetime import datetime

def parseFile(dataDir, fileName, groupName):
	filePath = dataDir + fileName
	councilNameEnd = fileName.find("_")
	councilName = fileName[:councilNameEnd]

	print(fileName)

	with open(filePath) as json_file:
		rows = []
		projectDataFields = (
			"StatVet",
			"BuildingType",
			"NumberLevels",
			"ClassifiedUse",
			"BuildingUse",
			"RestrictedWork",
		)

		try:
			data = json.load(json_file)
		except json.decoder.JSONDecodeError:
			print("Problem with JSON file, bad format: " + fileName)
			exit()

		# testLimit = 3
		# testCounter = 0

		for job in data:
			rfiCount = 0
			complexity = ""
			countBuildingApplications = len(job["project_building_data"])

			if "building_data" in job["project_data"] and len(job["project_data"]["building_data"]) > 0:
				complexity = job["project_data"]["building_data"][0]["Complexity"].strip()
				
				if len(job["project_data"]["building_data"][0]["rfi_documents"]) > 0:
					rfiCount = job["project_data"]["building_data"][0]["rfi_documents"][0]["rfi_count"]

			if (complexity not in group):
				continue

			fields = {
				"complexity": complexity,
				"application_type": job["application_type"],		
				"rfi_count": rfiCount,
			}
			
			if isinstance(job["project_data"], list):
				if len(job["project_data"]) > 0:
					for pdField in projectDataFields:
						if pdField in job["project_data"][0]:
							if pdField == "RestrictedWork":
								if job["project_data"][0][pdField].strip() == "y":
									fields[pdField] = "1"
								else:
									fields[pdField] = "0"
							else:
								fields[pdField] = job["project_data"][0][pdField]

						else:
							fields[pdField] = ""
				else:
					for pdField in projectDataFields:
						fields[pdField] = ""
			else:
				for pdField in projectDataFields:
					if pdField in job["project_data"]:
						if pdField == "RestrictedWork":
							if job["project_data"][pdField].strip() == "y":
								fields[pdField] = "1"
							else:
								fields[pdField] = "0"
						else:
							fields[pdField] = job["project_data"][pdField]
							
					else:
						fields[pdField] = ""

			rows.append(fields)

			# testCounter += 1
			# if testCounter > testLimit:
			# 	break	
			
		return rows


def writeCSVFile(outputFilePath, allRows):
	headerRow = allRows[0].keys()
	outputFile = open(outputFilePath, "a", newline="", encoding="utf-8")
	dictWriter = csv.DictWriter(outputFile, headerRow)
	dictWriter.writerows(allRows)
	outputFile.close()


def loopForAGroup(dataDir, outputDir, group):
	allRows = []

	testLimit = 30
	testCounter = 0
	csvFileName = "default.csv"

	excluded = (".", "..", "index.html")
	filesList = os.listdir(dataDir)
	for fileName in filesList:
		if fileName in excluded:
			continue
		
		# print(fullPathToFile)
		rows = parseFile(dataDir, fileName, group)
		allRows += rows

		
		testCounter += 1
		# if testCounter > testLimit:
		# 	break

		if testCounter == 1:
			# Write the first header row
			dateSuffix = datetime.now().strftime("%Y%m%d%H%M%S")
			headerRow = allRows[0].keys()
			csvFileName = outputDir + "alpha_export_" + dateSuffix + ".csv";

			outputFile = open(csvFileName, "a", newline="")
			dictWriter = csv.DictWriter(outputFile, headerRow)
			dictWriter.writeheader()
			outputFile.close()

		# Every 30 files, write info to the output file & clear the memory
		if testCounter % 30 == 0:
			writeCSVFile(csvFileName, allRows)
			allRows = []

	if len(allRows) > 0:
		writeCSVFile(csvFileName, allRows)


	print("Output file '" + csvFileName + "' written")


if __name__ == "__main__":
	dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021/"
	# dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/test/"
	outputDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/output/"
	
	groupNames = (
		("R1", "R2", "R3"),
		("C1", "C2", "C3")
	)

	for group in groupNames:
		loopForAGroup(dataDir, outputDir, group)
