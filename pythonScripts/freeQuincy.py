#!user/bin/python
import sys
#parse through every line of the file

#grab the number

#if it is in the dictionary
	#Grab the int it is associated with and += 1
#else 
	#add it to the dictionary and make the map = 1



inputFileLocation = '/fslgroup/fslg_genome/compute/cole/beweisen/output/blastFiles/'
outputFileName = '/fslgroup/fslg_genome/compute/cole/beweisen/output/blastAnalysis.txt'
speciesPrefix = 'd_'
filePostFix = '.blastout'
numArgs = len(sys.argv)


class FreeQuincy(object):
	#member fields
	speciesDictionaries = []
	speciesNames = []
	#member methods

	def makeOutputFile(self):
		self.f = open(outputFileName, "w+")

	def readInFiles(self):
	 	if (numArgs == 1):
			print "Please enter fastaFiles as command line arguments"
			return
		#cycle through all the input files
		for i in range(1, numArgs):

			#open new file
			inputFileName = inputFileLocation + sys.argv[i] #FIXME: ADD CODE TO BLASTBEE.PY
			inputFile = open(inputFileName,"r")
			
			#make a new dictionary
			bubbleFrequencies = {}
			bubbleFrequencies = self.parseInputFileForFrequencies(inputFile)

			#add the dictionary to the speciesDictionaries list
			self.speciesDictionaries.append(bubbleFrequencies)
			self.speciesNames.append(inputFileName.strip(filePostFix))

	def parseInputFileForFrequencies(self, file):
		bubFrequencies = {}
		for line in file:
			bubbleNumber = line.split("\t")[0]
			if bubbleNumber in bubFrequencies:
				freq = bubFrequencies[bubbleNumber]
				freq += 1
				bubFrequencies[bubbleNumber] = freq

			else:					
				#add the bubbleNumber to the dictionary
				bubFrequencies[bubbleNumber] = 1

		return bubFrequencies		
	def writeFrequenciesToFile(self):
		#FIXME: Fill in
		self.f.write("--Frequency Report--\n\n")	
		speciesCounter = 0;
		for dictionary in self.speciesDictionaries:
			numMultiMatches = 0	
			for k, v in dictionary.items():
				if v > 1:
					numMultiMatches += 1
			self.f.write("species: " + self.speciesNames[speciesCounter] + ":\n")
			self.f.write("     number of Bubbles total                                : " + str(len(dictionary)) + "\n")
			self.f.write("     number of bubles with multiple alignments              : " + str(numMultiMatches) + "\n")
			self.f.write("           bubbles with multiple alignments (bub, frequency):\n")
			for k, v in dictionary.items():
				if v > 1:
					self.f.write("                                                            " + str(k) + ", " + str(v) + "\n")
	def closeOutputFile(self):
		self.f.close()
	def printDictionary(self):
		print "*****************"
		for dictionary in self.speciesDictionaries:
			for k, v in dictionary.items():
				if v > 1:
					print v



fq = FreeQuincy()

fq.readInFiles()
fq.makeOutputFile()
fq.writeFrequenciesToFile()
fq.closeOutputFile()



