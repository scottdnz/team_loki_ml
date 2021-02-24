#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from lib.ExportFilesParser import ExportFilesParser

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

	efParser = ExportFilesParser(dataDir, outputDir, True)
	efParser.mainLoop(groupNames1)
	efParser.mainLoop(groupNames2)