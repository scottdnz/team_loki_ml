import os
import json
import csv
from datetime import datetime

def parseFile(dataDir, fileName, groupNames, projectDataFields, complexityMap, descriptionKeywords):
	filePath = dataDir + fileName
	councilNameEnd = fileName.find("_")
	councilName = fileName[:councilNameEnd]

	print(fileName)

	with open(filePath) as json_file:
		rows = []
		
		try:
			data = json.load(json_file)
		except json.decoder.JSONDecodeError:
			print("Problem with JSON file, bad format: " + fileName)
			exit()

		# testLimit = 3
		# testCounter = 0

		for job in data:
			complexityMatch = ""
			complexityVal = ""
			complexityCode = ""
			keywordFoundInDescription = "0"

			if "building_data" in job["project_data"] and len(job["project_data"]["building_data"]) > 0:
				complexityVal = job["project_data"]["building_data"][0]["Complexity"].strip()
				
				for code, complexities in groupNames.items():
					if complexityVal in complexities:
						complexityCode = str(code)
						break

				description = ""
				if "Description" in job["project_data"]["building_data"][0]:
					description = job["project_data"]["building_data"][0]["Description"]
				for keyword in descriptionKeywords:
					if description.lower().find(keyword) > -1:
						keywordFoundInDescription = "1"
						break

			if complexityCode == "":
				continue

			complexity = complexityMap[complexityVal]

			fields = {
				"complexity": complexity,
				"application_type": job["application_type"],
				"keyword_found_in_description": keywordFoundInDescription
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


def mainLoop(dataDir, outputDir, groupNames):
	allRows = []

	testLimit = 30
	testCounter = 0
	csvFileName = "default.csv"

	projectDataFields = (
		"NumberLevels",
		"ClassifiedUse",
		"BuildingUse",
		"RestrictedWork",
	)

	complexityMap = {
		"R1": 0,
		"R2": 1,
		"R3": 2,
		"C1": 0,
		"C2": 1,
		"C3": 2,
	}

	descriptionKeywords = ["Dwelling",
		"Fire",
		"Burner",
		"Office",
		"Commercial",
		"Factory",
		"Alteration",
		"Pool",
		"Garage",
		"Addition",
		"Storage",
		"Shop",
		"Level",
		"Complex",
		"Stage (For staged Commercial consents)",
		"Centre",
		"Mall",
		"Workshop",
		"Retail",
		"Complex"
	]
	for i in range(0, len(descriptionKeywords)):
		descriptionKeywords[i] = descriptionKeywords[i].lower()
		# print(descriptionKeywords)

	excluded = (".", "..", "index.html")
	filesList = os.listdir(dataDir)
	for fileName in filesList:
		if fileName in excluded:
			continue
		
		rows = parseFile(dataDir, fileName, groupNames, projectDataFields, complexityMap, descriptionKeywords)
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


def writeCSVFile(outputFilePath, allRows):
	headerRow = allRows[0].keys()
	outputFile = open(outputFilePath, "a", newline="", encoding="utf-8")
	dictWriter = csv.DictWriter(outputFile, headerRow)
	dictWriter.writerows(allRows)
	outputFile.close()


if __name__ == "__main__":
	dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021/"
	# dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/test/"
	outputDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/output/"
	
	groupNames1 = {
		"1": ("R1", "R2", "R3"),
	}
	groupNames2 = {
		"0": ("C1", "C2", "C3")
	}

	mainLoop(dataDir, outputDir, groupNames1)

	mainLoop(dataDir, outputDir, groupNames2)
