#!/usr/bin/env python3
import os
import time
import resource
import argparse
import numpy as np
import natsort as ns

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='path to sam file')
parser.add_argument('-r', type=int, default = 3, help='number of desired pseudoreplicates')
args = parser.parse_args()

alignfile = args.i
pseudo_reps = args.r

t1 = time.clock()

# Check alignment file is sorted
with open(alignfile, 'r') as handle:
    handle = handle.readlines()[-100:-1]
    qnames = []
    for line in handle:
        qname = line.partition("\t")[0]
        qnames.append(qname)
    if qnames != ns.natsorted(qnames):
        raise Exception("Please sort your alignment file by name. You can do this using samtools sort -n <file.sam> -o <sorted_file.sam>")

header = []
alignment_ids_init = set()
print('Your alignment file is being split')

# Open samfile, separate header lines, and create a set of qnames
with open(alignfile, 'r') as samfile:
    for line in samfile:
        if line[0] == "@":
            header.append(line)
        else:
            c1 = line.partition('\t')[0]
            alignment_ids_init.add(c1)

alignment_ids = ns.natsorted(alignment_ids_init)

# Create a new file for each replicate, and add the header
split_file_list = []
samfile_name, samfile_ext = os.path.splitext(alignfile)

for i in range(pseudo_reps):
    i += 1
    name = samfile_name + "_split" + str(i) + samfile_ext
    with open(name, "w") as samfile_split:
        split_file_list.append(name)
        for j in range(len(header)):
            samfile_split.write(header[j])

# generate a random integer for each unique alignment id (qname). This integer will ensure the alignemnt id goes to the correspoding pseudoreplicate file
alignment_outbound_id = []
alignment_outbound_int = []

#np.random.seed(args.s)   # doesn't work
for id in alignment_ids:
    pseudo_rep = np.random.randint(1,pseudo_reps+1)
    alignment_outbound_id.append(id)
    alignment_outbound_int.append(pseudo_rep)

alignment_outbound = list(zip(alignment_outbound_id, alignment_outbound_int))

# Add alignments to new file
with open(alignfile, 'r') as samfile:
    samfile = samfile.readlines()[len(header):]
    for row in samfile:
        r1 = row.partition("\t")[0]
        current_index = 0
        for id, rep in alignment_outbound[current_index:]:
            if id == r1:
                current_index = alignment_outbound.index((id,rep))
                with open(split_file_list[rep-1], 'a') as split_file_pseudorep:
                    split_file_pseudorep.write(row)
                break

t2 = time.clock()
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("time: " + str(round(t2-t1, 3)) + " sec")
print("memory: " + str(mem) + " Mb")
