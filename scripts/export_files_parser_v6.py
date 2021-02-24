import os
import json
import csv
from datetime import datetime


class ExportFilesParser:

	def __init__(self, dataDir, outputDir):
		self.dataDir = dataDir
		self.outputDir = outputDir


		self.projectDataFields = (
			"NumberLevels",
			"ClassifiedUse",
			"BuildingUse",
			"RestrictedWork",
		)

		self.complexityMap = {
			"R1": 0,
			"R2": 1,
			"R3": 2,
			"C1": 0,
			"C2": 1,
			"C3": 2,
		}

		self.descriptionKeywords = ["Dwelling",
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
		for i in range(0, len(self.descriptionKeywords)):
			self.descriptionKeywords[i] = self.descriptionKeywords[i].lower()


	def parseFile(self, fileName, groupNames):
		filePath = self.dataDir + fileName
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

				fields = {}
				for keyword in self.descriptionKeywords:
					keywordKey = "kw_" + keyword
					fields[keywordKey] = "0"


				if "building_data" in job["project_data"] and len(job["project_data"]["building_data"]) > 0:
					complexityVal = job["project_data"]["building_data"][0]["Complexity"].strip()
					
					for code, complexities in groupNames.items():
						if complexityVal in complexities:
							complexityCode = str(code)
							break

					description = ""
					if "Description" in job["project_data"]["building_data"][0]:
						description = job["project_data"]["building_data"][0]["Description"]
					for keyword in self.descriptionKeywords:
						if description.lower().find(keyword) > -1:
							keywordKey = "kw_" + keyword
							fields[keywordKey] = "1"

				if complexityCode == "":
					continue

				# print("complexityVal: " + complexityVal + ", complexityCode: " + complexityCode)
				complexity = self.complexityMap[complexityVal]

				fields["complexity"] = complexity
				fields["application_type"] = job["application_type"]
				
				if isinstance(job["project_data"], list):
					if len(job["project_data"]) > 0:
						for pdField in self.projectDataFields:
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
						for pdField in self.projectDataFields:
							fields[pdField] = ""
				else:
					for pdField in self.projectDataFields:
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


	def mainLoop(self, groupNames):
		allRows = []

		testLimit = 30
		testCounter = 0
		csvFileName = "default.csv"

		excluded = (".", "..", "index.html")
		filesList = os.listdir(self.dataDir)
		for fileName in filesList:
			if fileName in excluded:
				continue
			
			rows = self.parseFile(fileName, groupNames)
			allRows += rows

			testCounter += 1

			# Uncomment me for testing
			# if testCounter > testLimit:
			# 	break

			if testCounter == 1:
				# Write the first header row
				dateSuffix = datetime.now().strftime("%Y%m%d%H%M%S")
				headerRow = allRows[0].keys()
				csvFileName = self.outputDir + "alpha_export_" + dateSuffix + ".csv";

				outputFile = open(csvFileName, "a", newline="")
				dictWriter = csv.DictWriter(outputFile, headerRow)
				dictWriter.writeheader()
				outputFile.close()

			# Every 30 files, write info to the output file & clear the memory
			if testCounter % 30 == 0:
				self.writeCSVFile(csvFileName, allRows)
				allRows = []

		if len(allRows) > 0:
			self.writeCSVFile(csvFileName, allRows)


		print("Output file '" + csvFileName + "' written")


	def writeCSVFile(self, outputFilePath, allRows):
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

	efParser = ExportFilesParser(dataDir, outputDir)
	efParser.mainLoop(groupNames1)
	efParser.mainLoop(groupNames2)
