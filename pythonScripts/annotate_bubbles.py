#!/usr/bin/python

# Created by Kyle Johnsen, 1/17/18
# Takes aligned bubbles and annotation and creates a bubble annotation (.bann) file listing where bubbles are found, in the following 4-column format:
#
# 	bubble_id	  containing_gene  left_gene  right_gene  feature_cvg
#	...
#
# bubble_id
# containing_gene: the gene the bubble is located in. If there are multiple, gene symbols are separated with a semicolon
# left_gene: the gene on the left (lower bp coordinate) side if in an intergenic region
# right_gene: if intergenic, the gene on the right side (higher bp coordinate)
# feature_cvg: percent coverage of the feature--i.e., the gene or intergenic region--by the bubble sequence

# Input: three arguments:
# 	1 - .blastout file containing alignments for bubbles of interest
# 	2 - .gtf file containing genome annotation file for species of interest
# 	3 - desired output file location [stdout]


import gffutils
import sys
import subprocess
import os

# function for finding left and right surrounding genes. Starts immediately next to bubble
# and continues searching in that direction with windows of increasing width. Else report None
# bubble_region = ('chromosome', start, end)
# right_left: -1 for left, 1 for right
def get_surrounding_gene(gtf_db, bubble_region, left_side):
  chrom, start, end = bubble_region

  # prep for loop
  iter = 0
  search_width = 3000 * 2**iter # search region width increases exponentially
  search_start = start - search_width

  while search_width < 10**9:
    if left_side:
      if search_start < 0: # if it didn't find anything after already going negative last time, return None
        return None
      search_start = start - search_width
    else:
      search_start = end + 1
    search_end = search_start + search_width

    #print("Search start = %d  Search end = %d" % (search_start, search_end))
    results = list(gtf_db.region(region=(chrom, search_start, search_end)))
    iter += 1
    if len(results) > 0:
      # process results to find rightmost gene on left side and vice-versa
      if left_side:
        return sorted(results, key = lambda x: x.end, reverse=True)[0]
      else:
        return sorted(results, key = lambda x: x.start)[0]

    #prep for next iteration
    search_width = 3000 * 2**iter # search region width increases exponentially
    iter += 1

  return None

def get_left_gene(gtf_db, bubble_region):
  return get_surrounding_gene(gtf_db, bubble_region, True)

def get_right_gene(gtf_db, bubble_region):
  return get_surrounding_gene(gtf_db, bubble_region, False)

def get_containing_gene(gtf_db, bubble_region):
  results = list(gtf_db.region(region=bubble_region))
  return results


### PARSE ARGUMENTS
blast_file = sys.argv[1]
gtf_file = sys.argv[2]
try:
  out_file = sys.argv[3]
  output = open(out_file, 'w')
except IndexError:
  output = sys.stdout


### PARSE GTF FILE
## GUT GTF FILE TO INCLUDE ONLY GENES
tmp_file = "tmp.gtf"
subprocess.call("awk '$3==\"gene\"' %s > %s" % (gtf_file, tmp_file), shell=True)

## CALL GFFUTILS TO STORE GTF FILE
gtf_db = gffutils.create_db(tmp_file, dbfn='tmp.db', force=True, disable_infer_genes=True)
#gtf_db = gffutils.FeatureDB("tmp.db") # for faster debug


### PARSE BLASTOUT AND WRITE RESULTS
# blast output format: qseqid sseqid length score qstart qend sstart send
blast_file_handle = open(blast_file, 'r')
output.write("# bubble_id | containing_gene | left_gene | right_gene | feature_cvg (%)\n")
output.write("# -------------------------------------------------------------------------------\n")
for line in blast_file_handle:
  line = line.strip().split()
  bubble_id = line[0]
  bubble_region = (line[1], int(line[6]), int(line[7]))
  bubble_length = int(line[2])

  # if bubble in gene
  containing_gene = get_containing_gene(gtf_db, bubble_region)
  if len(containing_gene) != 0:
    gene_string = ";".join([x.attributes["gene_symbol"][0] for x in containing_gene])
    if bubble_region[1] < bubble_region[2]:
      bubble_start = bubble_region[1]
      bubble_end = bubble_region[2]
    else:
      bubble_start = bubble_region[2]
      bubble_end = bubble_region[1]
    # if the bubble spans multiple genes, calculate coverage based on start of first gene and end of last gene
    cg_start = int(containing_gene[0].start)
    cg_end = int(containing_gene[-1].end)
    assert cg_start < cg_end, "Apparently GTF file doesn't always have start come before end in genomic coordinates."
    # calculate based only on overlapping region: 
    # illustration   (  [ )        ]   where () is bubble and [] is containing gene(s)
    # overlapping region is only [)
    overlap_start = (cg_start if cg_start > bubble_start else bubble_start)
    overlap_end = (cg_end if cg_end < bubble_end else bubble_end)
    feature_cvg = (overlap_end - overlap_start + 1) / (cg_end - cg_start + 1) * 100 
    assert feature_cvg > 0, "Feature coverage shouldn't be negative"
    result_line = '\t'.join([str(x) for x in [bubble_id, gene_string, ".", ".", feature_cvg]])

  # if bubble in intergenic region
  else:
    left_gene = get_left_gene(gtf_db, bubble_region)
    left_gene_string = (left_gene.attributes["gene_symbol"][0] if left_gene != None else "None")
    right_gene = get_right_gene(gtf_db, bubble_region)
    right_gene_string = (right_gene.attributes["gene_symbol"][0] if right_gene != None else "None")
    try:
      feature_cvg = bubble_length / (int(right_gene.start) - int(left_gene.end) - 1)
    except AttributeError: # i.e., one or both of the genes is None
      feature_cvg = "."
    result_line = '\t'.join([str(x) for x in [bubble_id, '.', left_gene_string, right_gene_string, feature_cvg]])

  output.write(result_line + '\n')

blast_file_handle.close()
if output != sys.stdout:
  output.close()

#print(list(gtf_db.region(region=('2L', 779000, 783000), completely_within=True)))
#print(get_left_gene(gtf_db, ('2L', 781000, 781500)))
#print(get_right_gene(gtf_db, ('2L', 781000, 781500)))
#print(get_left_gene(gtf_db, ('X', 260000, 260500)))
#print(get_right_gene(gtf_db, ('X', 260000, 260500)))


### CLEANUP
os.remove(tmp_file)
os.remove('tmp.db')
