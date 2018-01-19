#!user/bin/python
import sys
import re
import subprocess

#   blatbee.py
#	commandline parameters: 
# 	blatbee.py fastaflie1.fa fastafile2.fa, etc.
#	make sure that each fasta file has the path going to it
#	The program can handle as many fasta files as desired

#prepare an sbatch script that blats each input file to every uploaded reference genome
#Runs the sbatch script
#stores the output in BlatSrc/twoBit
#


#FIXME: i need to find a way to upload the refference genomes. and we need a system for checking if they are .2bit or not, and if not, to put them in .2bit


numArgs = len(sys.argv)
#FIXME: I may want to add this one day as a way to make the program more flexible
#workingDirectory = subprocess.call('pwd', shell=True)

#FIXME: I hardcoded the outputfile location to be:
outputFileLocation = "/fslgroup/fslg_genome/compute/cole/beweisen/output/blastFiles/"
bubbleFileLocation = "/fslgroup/fslg_genome/compute/cole/beweisen/bubble_fasta_files/"
slurmScriptLocation = '/fslhome/bcb56/fsl_groups/fslg_genome/compute/cole/beweisen/slurmScripts/'
genomePrefix = "d_\w+"


class blaster(object):
	numRefGenomes  = 0
	numSBatchFiles = 0
	inputFastaFiles = []
	referenceGenomes = []
	outputFileNames = ''
	def __init__(self):
		return
	def runFreeQuincy(self):
		argument = 'python /fslgroup/fslg_genome/compute/cole/beweisen/pythonScripts/freeQuincy.py ' + self.outputFileNames
		subprocess.call(argument, shell = True)
	
		return
	def blastStringMaker(self, inputFileName):
		self.numSBatchFiles += 1

		refGenoGroup = re.search(genomePrefix, inputFileName) #THIS MAY HAVE A PROBLEM
		self.outputFileNames = self.outputFileNames + refGenoGroup.group(0) + ".blastout "
		referenceGenomePrefix = "/fslgroup/fslg_genome/compute/cole/beweisen/upload_user_files_here/ref_genomes_with_indexes/" + refGenoGroup.group(0)
		referenceGenome = "/fslgroup/fslg_genome/compute/cole/beweisen/upload_user_files_here/ref_genomes_with_indexes/" + refGenoGroup.group(0) + ".fasta"
		subprocessString = "module load blast/2.6.0\n"
		subprocessString = subprocessString + "cd /fslgroup/fslg_genome/compute/cole/beweisen/bubble_fasta_files/\n"
		subprocessString = subprocessString +  "makeblastdb -in " + referenceGenome + "  -parse_seqids -dbtype nucl\n"
		subprocessString = subprocessString + "time blastn -db " + referenceGenome + " -query " + bubbleFileLocation + inputFileName + " -out " + outputFileLocation + refGenoGroup.group(0) + ".blastout " + " -parse_deflines -outfmt \"6 qseqid sseqid length score qstart qend sstart send\"\n"
		return subprocessString
	def blastArgs(self):
		if (numArgs == 1):
			print "Please enter fastaFiles as command line arguments"
			return
		#cycle through all the input Fasta files
		for i in range(1, numArgs):
			#make an sbatch file for that fasta file
			inputFileName = sys.argv[i]
			self.inputFastaFiles.append(inputFileName)
			blastString = self.blastStringMaker(inputFileName)
			subprocess.call(blastString, shell=True)		
	
		return



machine = blaster()
machine.blastArgs()
machine.runFreeQuincy()

