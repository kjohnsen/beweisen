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
outputFileLocation = "/fslgroup/fslg_genome/compute/cole/beweisen/output/"
slurmScriptLocation = '/fslhome/bcb56/fsl_groups/fslg_genome/compute/cole/beweisen/slurmScripts/'



#/fslhome/bcb56/fsl_groups/fslg_genome/compute/cole/blat/blatSrc/twoBit
class blatter(object):
	numRefGenomes  = 0
	numSBatchFiles = 0
	sBatchFiles = []
	inputFastaFiles = []
	referenceGenomes = []
	def __init__(self):
		return
#	def addReferenceGenome(self, fileName):
#		self.numRefGenomes += 1
#		self.referenceGenomes.append(fileName)
#		return
	def getSBatchFiles(self):
		for i in range(0, self.numSBatchFiles):
			print self.sBatchFiles[i]
		return
	def runSBatchFiles(self):
		print "number of sbatch files: " + str(self.numSBatchFiles)
		print "performing a bwa the following files on Marylou:\n"
		for i in range(0, self.numSBatchFiles):
			print self.sBatchFiles[i] + "\n"
			subprocess.call('sbatch ' + self.sBatchFiles[i], shell=True)
		print "the sorted .bam files can be found in  " + slurmScriptLocation

		return
	def sBatchFileMaker(self, inputFileName):
		self.numSBatchFiles += 1
		f = open("/fslgroup/fslg_genome/compute/cole/beweisen/slurmScripts/slurmScript" + str(self.numSBatchFiles) + "_of_" + str(self.numSBatchFiles) + ".sh", "w+")
		#f = open(("blatScript." + inputFileName + ".sh"), "w+") #It would be nice to hang on to these somehow. Maybe through making this an object
		f.writelines("#!/bin/bash\n")
		f.writelines("#SBATCH --time=00:30:00   # walltime\n")
		f.writelines("#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)\n")
		f.writelines("#SBATCH --nodes=1   # number of nodes\n")
		f.writelines("#SBATCH --mem-per-cpu=8G   # memory per CPU core\n")
		f.writelines("#SBATCH --mail-user=brian27.byu@gmail.com   # email address\n")
		f.writelines("#SBATCH --mail-type=BEGIN\n")
		f.writelines("#SBATCH --mail-type=END\n")
		f.writelines("#SBATCH --mail-type=FAIL\n")
#		f.writelines("# Compatibility variables for PBS. Delete if not needed.\n")
#		f.writelines("export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`\n")
#		f.writelines("export PBS_JOBID=$SLURM_JOB_ID\n")
#		f.writelines("export PBS_O_WORKDIR=\"$SLURM_SUBMIT_DIR\"\n")
#		f.writelines("export PBS_QUEUE=batch\n")
#		f.writelines("# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.\n")
#		f.writelines("export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE\n")
		f.writelines("# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE\n")
		#/fslgroup/fslg_genome/compute/cole/blat/blatSrc/twoBit	
		refGenoGroup = re.search('d_\w+', inputFileName) #THIS MAY HAVE A PROBLEM
		referenceGenomePrefix = "/fslgroup/fslg_genome/compute/cole/beweisen/upload_user_files_here/ref_genomes_with_indexes/" + refGenoGroup.group(0)
		referenceGenome = "/fslgroup/fslg_genome/compute/cole/beweisen/upload_user_files_here/ref_genomes_with_indexes/" + refGenoGroup.group(0) + ".fasta"
		#REPLACE THIS WITH BWS
		#load the modules
		f.writelines("module load blast/2.6.0\n\n")
		f.writelines("cd /fslgroup/fslg_genome/compute/cole/beweisen/bubble_fasta_files/\n\n")
		f.writelines("makeblastdb -in " + referenceGenome + "  -parse_seqids -dbtype nucl\n\n")
		#Index the reference genomes
		f.writelines("time blastn -db " + referenceGenome + " -query " + referenceGenome + " -out " + outputFileLocation + str(self.numSBatchFiles) + ".blastout " + " -outfmt \"6 qacc sacc qseqid sseqid sstart send\"\n\n")
		#view the alginemtsn in teh terminal
		#FIME: FINISH THIS STUFF :)
#		newFileName = inputFileName.strip("fasta")
#		f.writelines("blastn " + " -query " + inputFileName + " -db " + referenceGenome + " -out " + outputFileLocation + "/" + newFileName + "blastput\n\n")
	#	f.writelines("blat " + referenceGenome + " " + inputFileName + " " +  outputFileLocation + "/" + newFileName + "psl\n\n")
	#	f.writelines("pslPretty " + outputFileLocation + "/" + newFileName + "psl" + " " + referenceGenome + " " + inputFileName + " " + newFileName + "prettyCool.out")
		#FIXME: update this to output the output files numbered, and with the SPECIES NAME added on.

	def readArgs(self):
		if (numArgs == 1):
			print "Please enter fastaFiles as command line arguments"
			return
		#cycle through all the input Fasta files
		for i in range(1, numArgs):
			#print sys.argv[i]
			#make an sbatch file for that fasta file
			inputFileName = sys.argv[i]
			self.inputFastaFiles.append(inputFileName)
			self.sBatchFileMaker(inputFileName)			
			#Add that sBatchFile to the List
			slurmScriptPrefix = '/fslhome/bcb56/fsl_groups/fslg_genome/compute/cole/beweisen/slurmScripts/'
			self.sBatchFiles.append(slurmScriptLocation + "slurmScript" + str(i) + "_of_" + str(self.numSBatchFiles) + ".sh")
#		for i in range(0, numArgs - 1):
#			print self.inputFastaFiles[i] + "\n"

	
		return



machine = blatter()
#machine.addReferenceGenome(referenceGenome1)
#machine.addReferenceGenome(referenceGenome2)
#machine.addReferenceGenome(referenceGenome3)
#machine.addReferenceGenome(referenceGenome4)
#machine.addReferenceGenome(referenceGenome5)
#machine.addReferenceGenome(referenceGenome6)
#machine.addReferenceGenome(referenceGenome7)
#machine.addReferenceGenome(referenceGenome8)
#machine.addReferenceGenome(referenceGenome9)
#machine.addReferenceGenome(referenceGenome10)
#machine.addReferenceGenome(referenceGenome11)
#machine.addReferenceGenome(referenceGenome12)

machine.readArgs() #make sbatchFiles for each input fasta file
#machine.runSBatchFiles() #run SBatch files
print "sbatch output can be found in: " + slurmScriptLocation



