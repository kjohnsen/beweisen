#!/usr/bin/python3

# Analyzes bubble annotation files across all species and produces a report by bubble with the following format
#
# bubble_id | concordance | bubbles_mapped(%) | ortholog_group_1:% | ortholog_group_2:% | ortholog_group_3:%...
#
# where "ortholog_group"s are sorted in descending order of proportion of matches
# and concordance = bubbles_mapped * (ortholog_group_1 proportion)

# Input is as follows: ortholog_table_file species_1.bann[ species_2.bann species_3.bann...]
# Output is to stdout

# Created 1/29/18, Kyle Johnsen


import sys
from collections import defaultdict
import os

# returns dictionary of gene_symbol:ortholog_group
def parse_FB_orthologs(filename):
  return ortho_dict

### INPUTS
ortho_dict = parse_FB_orthologs(sys.argv[1])
bubble_annotations = sys.argv[2:]

### READ BUBBLE ANNOTATION FILES
results_dict = defaultdict(lambda: defaultdict(int))
for filename in bubble_annotations:
  bann = file.open(filename, "r")
  for line in bann:
    if line[0] == "#": 
      continue
    line = line.strip().split('\t')
    # if genic
      # if multiple genes
    # if intergenic

  bann.close()
