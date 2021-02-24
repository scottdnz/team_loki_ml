"""
    ExportFilesParser
    ~~~
    This module contains functions that parse a set of JSON data files. It processes 
    each one and converts its info into a set of CSV rows. For every X data file 
    read, it will append CSV rows to the end of a CSV output file that is 
    written as it goes.
   
    :copyright: (c) 2021 by Scott Davies for Objective Corporation.
"""

import os
import json
import csv
from datetime import datetime

class ExportFilesParser:

	def __init__(self, dataDir, outputDir, testMode=False):
		"""Constructor.
		:param datadir: string.
		:param outpurdir: string.
		:param testMode: bool.
		"""
		self.dataDir = dataDir
		self.outputDir = outputDir
		self.testMode = testMode


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


	def addProjectDataFields(self, fields, projectData):
		"""
		:param fields: dict
		:param projectData: list/dict of JSON data
		:return fields: the keys & values for a CSV output row.
		:rtype: dict
		"""
		if isinstance(projectData, list):
			if len(projectData) > 0:
				for pdField in self.projectDataFields:
					if pdField in projectData[0]:
						if pdField == "RestrictedWork":
							if projectData[pdField].strip() == "y":
								fields[pdField] = "1"
							else:
								fields[pdField] = "0"
						else:
							fields[pdField] = projectData[0][pdField]

					else:
						fields[pdField] = ""
			else:
				for pdField in self.projectDataFields:
					fields[pdField] = ""
		else:
			for pdField in self.projectDataFields:
				if pdField in projectData:
					if pdField == "RestrictedWork":
						if projectData[pdField].strip() == "y":
							fields[pdField] = "1"
						else:
							fields[pdField] = "0"
					else:
						fields[pdField] = projectData[pdField]
						
				else:
					fields[pdField] = ""
		return fields


	def getBinnedRFIDocsCount(self, rfiCountOriginal):
		"""
		:param rfiCountOriginal: int.
		:return: rfiCount
		:rtype:int.
		"""
		rfiCount = rfiCountOriginal
		if rfiCountOriginal >= 10:
			rfiCount = 10
		return rfiCount


	def parseFile(self, fileName, groupNames):
		"""
		Reads one JSON source file and extracts its info for CSV output rows.
		:param fileName: string.
		:param groupNames: tuple.
		:return rows: CSV data.
		:rtype: list.
		"""
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
				rfiCountOriginal = 0

				fields = {}
				for keyword in self.descriptionKeywords:
					keywordKey = "kw_" + keyword
					fields[keywordKey] = "0"


				if "building_data" in job["project_data"] and \
						len(job["project_data"]["building_data"]) > 0:
					complexityVal = job["project_data"]["building_data"][0]["Complexity"].strip()
					
					for code, complexities in groupNames.items():
						if complexityVal in complexities:
							complexityCode = str(code)
							break

					description = ""
					if "Description" in job["project_data"]["building_data"][0]:
						description = job["project_data"]["building_data"][0]["Description"].lower()
					for keyword in self.descriptionKeywords:
						if description.find(keyword) > -1:
							keywordKey = "kw_" + keyword
							fields[keywordKey] = "1"

					if "rfi_documents" in job["project_data"]["building_data"][0] and \
							len(job["project_data"]["building_data"][0]["rfi_documents"]) > 0:
						rfiCountOriginal = job["project_data"]["building_data"][0]["rfi_documents"][0]["rfi_count"]

				if complexityCode == "":
					continue

				# print("complexityVal: " + complexityVal + ", complexityCode: " + complexityCode)
				complexity = self.complexityMap[complexityVal]

				fields["complexity"] = complexity
				fields["application_type"] = job["application_type"]
				fields["rfi_count"] = self.getBinnedRFIDocsCount(rfiCountOriginal)

				fields = self.addProjectDataFields(fields, job["project_data"])

				rows.append(fields)

				# testCounter += 1
				# if testCounter > testLimit:
				# 	break	
				
			return rows


	def mainLoop(self, groupNames):
		"""
		:param groupNames: tuple.
		"""
		allRows = []

		if self.testMode == True:
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
			if self.testMode == True and testCounter > testLimit:
				break

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
		"""
		:param outputFilePath: string.
		:param allRows: list.
		"""
		headerRow = allRows[0].keys()
		outputFile = open(outputFilePath, "a", newline="", encoding="utf-8")
		dictWriter = csv.DictWriter(outputFile, headerRow)
		dictWriter.writerows(allRows)
		outputFile.close()
