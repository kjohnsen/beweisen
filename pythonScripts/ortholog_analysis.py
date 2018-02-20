#!/usr/bin/python3

# Analyzes bubble annotation files across all species and produces a report by bubble with 
# the following tab-delimited format
#
# bubble_id | concordance | species_mapped(%) | map_count_avg | ortholog_group_1:% | ortholog_group_2:% | ortholog_group_3:%...
#
# where "ortholog_group"s are sorted in descending order of proportion of matches:
# that is, what percentage of species mapped to that group
# and concordance = biggest ortholog group [group 1] proportion
#
# map_count_avg is how many times a bubble mapped for each species, on average. We would expect 1.

# Input is as follows: ortholog_table_file species_1.bann[ species_2.bann species_3.bann...]
# Output is to stdout

# Ortholog group proportions are calculated as a percentage of a total of #species*2
# where groups for genic bubbles count twice. For example, for two bubbles, one 
# in gene1 and the other between gene2 and gene3, ortholog_group_1 would have a value
# of 2/4 = 50%. Where a genic bubble covers multiple genes, the ortholog group of 
# each gene gets counted twice just as for other genic bubbles

# Created 1/29/18, Kyle Johnsen


from collections import defaultdict
import os
import sys


# key dependent defaultdict needed to return the gene symbol itself when an ortholog
# group isn't found
class key_dependent_defdict(defaultdict):
  def __init__(self, fxn):
    super().__init__(None)
    self._fxn = fxn
  def __missing__(self, key):
    ret = self._fxn(key)
    self[key] = ret
    return ret


# returns dictionary of gene_symbol:ortholog_group
def parse_FB_orthologs(filename):
  ortho_dict = key_dependent_defdict(lambda key: key)
  ortho_file = open(filename, 'r')
  current_d_mel_gene = "."
  for line in ortho_file:
    if line[0] == "#": continue
    line = line.strip().split()
    if len(line) == 0: continue
    assert len(line) == 11
    ortho_group = line[10]
    # if d_mel gene encountered for first time, add it to dictionary
    if line[1] != current_d_mel_gene:
      current_d_mel_gene = line[1]
      ortho_dict[current_d_mel_gene] = ortho_group
    ortho_dict[line[6]] = ortho_group
  ortho_file.close()
  return ortho_dict


### INPUTS
ortho_dict = parse_FB_orthologs(sys.argv[1])
bubble_annotations = sys.argv[2:]


### READ BUBBLE ANNOTATION FILES
results_dict = defaultdict(lambda: defaultdict(int))
num_species = len(bubble_annotations)
species_per_bubble_dict = defaultdict(lambda: [False]*num_species)
i = 0
for filename in bubble_annotations:
  bann = open(filename, "r")
  for line in bann:
    if line[0] == "#": 
      continue
    line = line.strip().split('\t')
    bubble_id = line[0]

    # keep track of what species have map for this bubble
    species_per_bubble_dict[bubble_id][i] = True

    # if genic
    if line[1] != ".":
      genes = line[1].split(';')
      for gene in genes:
        ortho_group = ortho_dict[gene]
        results_dict[bubble_id][ortho_group] += 2

    # if intergenic
    else:
      side_genes = line[2:4]
      for gene in side_genes:
        if gene == "None": continue
        ortho_group = ortho_dict[gene]
        results_dict[bubble_id][ortho_group] += 1

  bann.close()
  i += 1


### PRINT RESULTS
print("## bubble_id | concordance | species_mapped(%) | map_count_avg | ortholog_group_1:% | ortholog_group_2:%...")
print("## -------------------------------------------------------------------------------------")
for (bubble_id, group_counter) in results_dict.items():
  ortho_groups_sorted = sorted(group_counter.items(), key=lambda x:x[1], reverse=True)
  total_group_count = sum([x[1] for x in ortho_groups_sorted])
  species_mapped = sum(species_per_bubble_dict[bubble_id])
  species_mapped_percent = species_mapped / num_species * 100
  assert species_mapped_percent >= 0 and species_mapped_percent <= 100
  concordance = ortho_groups_sorted[0][1] / (num_species * 2) * 100
  map_count_avg = total_group_count / (species_mapped * 2)
  bubble_results = "{:s}\t{:.2f}\t{:.2f}\t{:.2f}\t".format(bubble_id, concordance, species_mapped_percent, map_count_avg)
  bubble_results = bubble_results + '\t'.join(["{:s}:{:.2f}".format(x[0], x[1]/(num_species * 2)*100) for x in ortho_groups_sorted])
  print(bubble_results)


