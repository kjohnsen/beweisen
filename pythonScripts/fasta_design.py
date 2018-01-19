import collections	
import subprocess

# 	param: Fasta file of each de bruijn bubble for a collection
#		of species
#	return: a list of files, one file for each species, containing each bubble
#		with its correcponding bubble

file = open('/fslgroup/fslg_genome/compute/cole/beweisen/upload_user_files_here/bubbles.out/super.bubbles.out')
collection = {}
checkLine = False
for line in file:
	if line[0] == '>':
		species_list = []
		line = line.strip() 
		bubble_count = line.split()[2]
		subString = line.split()[4]
		if subString[-1] == ',':
			species_list.append(subString[:-1])
		else:
			species_list.append(subString)
		for word in line.split(", ")[1:]:
			species_list.append(word)
		checkLine = False
	else:
		bubble = line.strip()
		checkLine = True
	if checkLine == True:
		for species in species_list:
			if species in collection:
				collection[species][bubble_count] = bubble
			else:
				collection[species] = {}
				collection[species][bubble_count] = bubble
outputList = []
file_names = ''
bubbleFastaPrefix = '/fslgroup/fslg_genome/compute/cole/beweisen/bubble_fasta_files/'
for key in collection.keys():
	outputFile = key
	
	out = open(bubbleFastaPrefix + '%s%s' % (key, '.bubble.fasta'),'w')
	file_names = file_names + '%s%s' % (key, '.bubble.fasta')
	file_names = file_names + ' '
	bubble_num = collection[key].keys()
	keys = []
	for numb in bubble_num:
		keys.append(int(numb))
	keys.sort()
	for bubble_number in keys:
		bubble_number = str(bubble_number)
		out.write('>lcl|' + bubble_number + " " +  key +'\n' + collection[key][bubble_number] + '\n')#.format(num, key, (collection[key][num])))
	outputList.append(out)
argument = 'python /fslgroup/fslg_genome/compute/cole/beweisen/pythonScripts/blastbee.py ' + file_names[:-1]
subprocess.call(argument, shell = True)
