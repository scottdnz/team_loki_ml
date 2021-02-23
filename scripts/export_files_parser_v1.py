import os
import json
import csv
from datetime import datetime

def parseFile(dataDir, fileName):

	filePath = dataDir + fileName
	councilNameEnd = fileName.find("_")
	councilName = fileName[:councilNameEnd]

	print(fileName)

	with open(filePath) as json_file:
		rows = []
		projectDataFields = (
				"Description",
				"ExistingArea",
				"ResBedrooms",
				"NewArea",
				"StatVet",
				"BuildingType",
				"NumberLevels",
				"NumberUnits",
				"ClassifiedUse",
				"BuildingUse",
				"EstimatedValue",
				"RestrictedWork",
				"ResidentialBuildingContract",
			)

		try:
			data = json.load(json_file)
		except json.decoder.JSONDecodeError:
			print("Problem with JSON file, bad format: " + fileName)
			exit()

		# testLimit = 3
		# testCounter = 0

		for job in data:
			workType = ""
			useCode = ""
			rfiCount = 0
			ownerBuilder = ""
			complexity = ""
			PBBuildingType = ""
			buildingLife = ""

			jobID = ""
			if "JID" in job["project_data"]:
				jobID = job["project_data"]["JID"]
			
			countBuildingApplications = len(job["project_building_data"])
			if countBuildingApplications > 0 and job["project_building_data"][0]["building_use_data"]:
				workType = job["project_building_data"][0]["building_use_data"]["work_type"]
				useCode = job["project_building_data"][0]["building_use_data"]["use_code"]
				ownerBuilder = job["project_building_data"][0]["pb_owner_builder"]
				PBBuildingType = job["project_building_data"][0]["pb_bldg_type"]
				buildingLife = job["project_building_data"][0]["pb_bldg_life"]

			if "building_data" in job["project_data"] and len(job["project_data"]["building_data"]) > 0:
				complexity = job["project_data"]["building_data"][0]["Complexity"]
				
				if len(job["project_data"]["building_data"][0]["rfi_documents"]) > 0:
					rfiCount = job["project_data"]["building_data"][0]["rfi_documents"][0]["rfi_count"]

			fields = {
				"job_id": jobID,
				"application_type": job["application_type"],
				"is_compliance_schedule": job["is_compliance_schedule"],
				"owner_builder": ownerBuilder,
				"work_type": workType, 
				"use_code": useCode,
				"complexity": complexity,
				"rfi_count": rfiCount,
				"pb_bldg_type": PBBuildingType,
				"building_life": buildingLife,
				"means_compliance_count": len(job["means_compliance"]),
				"compliance_schedules_count": len(job["compliance_schedules_v2"]),
				"max_occupant_load": str(job["max_occupant_load"]),
				"building_applications_count": countBuildingApplications,
				"council_name": councilName
			}
			
			if isinstance(job["project_data"], list):
				if len(job["project_data"]) > 0:
					for pdField in projectDataFields:
						if pdField in job["project_data"][0]:
							fields[pdField] = job["project_data"][0][pdField]
						else:
							fields[pdField] = ""
				else:
					for pdField in projectDataFields:
						fields[pdField] = ""
			else:
				for pdField in projectDataFields:
					if pdField in job["project_data"]:
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


if __name__ == "__main__":
	dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021/"
	# dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/test/"
	outputDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/output/"

	allRows = []

	# testLimit = 30
	testCounter = 0
	csvFileName = "default.csv"

	excluded = (".", "..", "index.html")
	filesList = os.listdir(dataDir)
	for fileName in filesList:
		if fileName in excluded:
			continue
		
		# print(fullPathToFile)
		rows = parseFile(dataDir, fileName)
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
