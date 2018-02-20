#!/usr/bin/python

'''
Takes two arguments: the file with all the bubbles and a file with only the bubbles to keep, one number per line
Output to stdout
Feb 12, 2018, Kyle Johnsen
'''

import sys
from Bio import SeqIO, AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

bubble_file = sys.argv[1]
bubble_selection = sys.argv[2]

bubbles_to_keep = set()
with open(bubble_selection, 'r') as fh:
    for line in fh:
        bubbles_to_keep.add(int(line.strip()))

with open(bubble_file, 'r') as fh:
    for record in SeqIO.parse(fh, 'fasta'):
        tokens = record.description.strip().split()
        bubble_num = int(tokens[1])
        if bubble_num not in bubbles_to_keep:
            continue
        else:
            SeqIO.write(record, sys.stdout, "fasta")
