import os
import json

def parseFile(filePath):
	with open(filePath) as json_file:
		rows = []

		data = json.load(json_file)

		testLimit = 1
		testCounter = 0

		for job in data:
			workType = ""
			useCode = ""
			rfiCount = 0

			if (job["project_building_data"][0]["building_use_data"]):
				workType = job["project_building_data"][0]["building_use_data"]["work_type"]
				useCode = job["project_building_data"][0]["building_use_data"]["use_code"]

			if len(job["project_data"]["building_data"][0]["rfi_documents"]) > 0:
				rfiCount = job["project_data"]["building_data"][0]["rfi_documents"][0]["rfi_count"]

			fields = {
				"job_id": job["project_data"]["JID"],
				"owner_builder": job["project_building_data"][0]["pb_owner_builder"],
				"work_type": workType, 
				"use_code": useCode,
				"complexity": job["project_data"]["building_data"][0]["Complexity"],
				"rfi_count": rfiCount,
				"description": job["project_data"]["Description"],
				"existing_area": job["project_data"]["ExistingArea"],
				"new_area": job["project_data"]["NewArea"],
				"stat_vet": job["project_data"]["StatVet"],
				"building_type": job["project_data"]["BuildingType"],
				"number_levels": job["project_data"]["NumberLevels"],
				"number_units": job["project_data"]["NumberUnits"],
				"classified_use": job["project_data"]["ClassifiedUse"],
				"building_use": job["project_data"]["BuildingUse"],
				"estimated_value": job["project_data"]["EstimatedValue"],
				"restricted_work": job["project_data"]["RestrictedWork"],
				"residential_building_contract": job["project_data"]["ResidentialBuildingContract"],
				"compliance_schedules_count": len(job["compliance_schedules_v2"]),
				"max_occupant_load": job["max_occupant_load"]
			}

			print(fields)


			testCounter += 1
			if testCounter > testLimit:
				break	

			print("****")

			rows.append(fields)
			
		return rows


def writeCSVFile():
	with open('people.csv', 'w', newline='')  as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(toCSV)


if __name__ == "__main__":
	dataDir = "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021/"

	allRows = []

	testLimit = 1
	testCounter = 0

	excluded = (".", "..")
	filesList = os.listdir(dataDir)
	for fileName in filesList:
		if fileName in excluded:
			continue
		fullPathToFile = dataDir + fileName
		# print(fullPathToFile)
		rows = parseFile(fullPathToFile)
		allRows += rows

		
		testCounter += 1
		if testCounter > testLimit:
			break

	print(allRows)