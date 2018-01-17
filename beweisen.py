##!user/bin/python
import subprocess
import sys

#Clear the output and temporary folders
argument = 'rm -r slurmScripts'
subprocess.call(argument, shell = True)

argument = 'mkdir slurmScripts'
subprocess.call(argument, shell = True)

argument = 'rm -r bubble_fasta_files'
subprocess.call(argument, shell = True)

argument = 'mkdir bubble_fasta_files'
subprocess.call(argument, shell = True)

argument = 'rm -r output'
subprocess.call(argument, shell = True)

argument = 'mkdir output'
subprocess.call(argument, shell = True)

#
argument = 'python ./pythonScripts/fasta_design.py'
subprocess.call(argument, shell = True)

