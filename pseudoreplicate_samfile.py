#!/usr/bin/env python3
import os
import datetime
import argparse
import numpy as np

print('Your sam file is being split')
print("Started at: " + str(datetime.datetime.now()))

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='path to sam file')
parser.add_argument('-r', type=int, default = 3, help='number of desired pseudoreplicates')
parser.add_argument('-s', type=int, default=None, help='set a seed for reproducibility')
args = parser.parse_args()

alignfile = args.i

header = []
alignment_ids = set()

# Open samfile, separate header lines, and create a set of qnames
with open(alignfile, 'r') as samfile:
    for line in samfile:
        if line[0] == "@":
            header.append(line)
        else:
            c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16 = line.split('\t')
            alignment_ids.add(c1)

# Create a new file for each replicate, and add the header
split_file_list = []
samfile_name, samfile_ext = os.path.splitext(alignfile)
pseudo_reps = args.r

for i in range(pseudo_reps):
    i += 1
    name = samfile_name + "_split" + str(i) + samfile_ext
    with open(name, "w") as samfile_split:
        split_file_list.append(name)
        for j in range(len(header)):
            samfile_split.write(header[j])

# Generate a random integer for each unique alignment id (qname). This integer will ensure the alignemnt record goes to the correspoding pseudoreplicate file
alignment_outbound = {}

np.random.seed(args.s)
for id in alignment_ids:
    pseudo_rep = np.random.randint(1,pseudo_reps+1)
    alignment_outbound[id] = pseudo_rep

# Add alignments to new file
for id, rep in alignment_outbound.items():
    with open(alignfile, 'r') as samfile:
        samfile = samfile.readlines()[len(header):]
        for row in samfile:
            r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16 = row.split('\t')
            if id == r1:
                with open(split_file_list[rep-1], 'a') as split_file_pseudorep:
                    split_file_pseudorep.write(row)

print("Finished at: " + str(datetime.datetime.now()))
