#!/usr/bin/python

# Created by Kyle Johnsen, 1/17/18
# Takes aligned bubbles and annotation and creates a summary file listing where bubbles are found, in the following 4-column format:
#
# 	bubble_id	in/left_gene	right_gene	feature_cvg
#	...
#
# bubble_id
# in/left_gene: the gene the bubble is located in, or on the left (lower bp coordinate) side if in an intergenic region
# right_gene: if intergenic, the gene on the right side (higher bp coordinate)
# feature_cvg: percent coverage of the feature--i.e., the gene or intergenic region--by the bubble sequence

# Input: three arguments:
# 	1 - .blastout file containing alignments for bubbles of interest
# 	2 - .gtf file containing genome annotation file for species of interest
# 	3 - desired output file location [stdout]

import gffutils

### PARSE GTF FILE


### PARSE BLASTOUT AND WRITE RESULTS

