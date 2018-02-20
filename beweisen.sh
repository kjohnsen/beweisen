#!/bin/bash
# created 1/24/18
# Runs fasta_design.py
# then iterates over bubble files, then run for each species the following:
# blastbee.py
# annotate_bubbles.py
# ??? stuff to check orthologs and get other statistics like genome coverage


home_path="/fslgroup/fslg_genome/compute/cole/beweisen/"
cd $home_path

# Clear the output and temporary folders
#rm -r slurmScripts
#mkdir slurmScripts
#rm -r bubble_fasta_files
#mkdir bubble_fasta_files
#rm -r output
#mkdir output
#mkdir output/blastFiles
rm -r output/bubbleAnnotations
mkdir output/bubbleAnnotations




### RUN SCRIPTS

#python3 pythonScripts/fasta_design.py

basenames=$(ls bubble_fasta_files | sed -n 's/\.bubble\.fasta//p')
fasta_files=$(ls bubble_fasta_files)

#python3 blastbee.py $fasta_files

for bn in $basenames
do
  python3 pythonScripts/annotate_bubbles.py output/blastFiles/10/${bn}.mutual upload_user_files_here/gtf_files/${bn}.gtf output/bubbleAnnotations/${bn}.bann
done

python3 pythonScripts/ortholog_analysis.py upload_user_files_here/ort
upload_user_files_here/ortholog_table/gene_orthologs_fb_2015_03.tsv
