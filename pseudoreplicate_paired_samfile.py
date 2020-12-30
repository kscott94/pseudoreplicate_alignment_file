#!/usr/bin/env python3
import os
import time
import resource
import argparse
import pysam as pys
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='path to sam file')
parser.add_argument('-r', type=int, default = 3, help='number of desired pseudoreplicates')
parser.add_argument('-s', type = int, default=None, help='set seed')
parser.add_argument('-b', action = 'store_true', help='output files in bam format, sorted by coordinate')

args = parser.parse_args()

in_file = args.i
pseudo_replicates = args.r

t1 = time.clock()

in_file_name, in_file_ext = os.path.splitext(in_file)

# Check file extension
if not args.b and in_file_ext == ".bam":
    print('Your file must have a .sam extension.')
    print('If you are using a bam file, use -b flag.')
    exit(0)

# Sort alignment file by name
alignfile = str(in_file_name) + "_nsorted_tmp.sam"
pys.sort("-o", alignfile, "-n", in_file)

print('Getting ready...')

# Open samfile, separate header lines, and create a set of qnames
header = []
read_count = 0

with open(alignfile, 'r') as f:
    for line in f.readlines():
        if line[0] == "@":
            header.append(line)
        else:
            read_count +=1

print('Your alignment file is being split...')

# Create a new file for each replicate, and add the header
split_file_list = []

for i in range(pseudo_replicates):
    i += 1
    if args.b:
        name = in_file_name + "_split" + str(i) + ".bam"
    else:
        name = in_file_name + "_split" + str(i) + ".sam"
    with open(name, "w") as samfile_split:
        split_file_list.append(name)
        for j in range(len(header)):
            samfile_split.write(header[j])

# Add alignments to new file
with open(alignfile, 'r') as f:
    samfile = f.readlines()[len(header):]     # start reading file at first read

    # Write the first read into a split file
    with open(split_file_list[0], 'a') as f1:
        f1.write(samfile[0])

    # Initialize parameters for the rest of the reads
    index = 1  # The first read is at index 0. Starting at
    int = 0    # The first file containing reads is called _split1.sam
    # Begin partitioning reads into files randomly, keeping pairs together
    np.random.seed(args.s)  # doesn't work
    for i in range(read_count-1):
        if samfile[index].partition("\t")[0] == samfile[index-1].partition("\t")[0]:
            with open(split_file_list[int], 'a') as f2:
                f2.write(samfile[index])
        else:
            int = np.random.randint(pseudo_replicates)
            with open(split_file_list[int], 'a') as f3:
                f3.write(samfile[index])
        index += 1

#convert output to bam is args.b, and remove all temp files
if args.b:
    print('Converting sam to bam...')
    print('Sorting by coordinate...')
    for file in split_file_list:
        name, ext = os.path.splitext(file)
        split_out_name = str(name) + '.bam'
        pys.sort("-o", split_out_name, file)

os.remove(alignfile)

t2 = time.clock()
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("time: " + str(round(t2-t1, 3)) + " sec")
print("memory: " + str(mem) + " Mb")
