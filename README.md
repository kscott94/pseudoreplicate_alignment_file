# pseudoreplicate BAM file
This python script allows you to randomly split a sequence alignment file into several smaller files, called pseudoreplicates. Paired end reads will be retained within the same file. Also compatible with non-paired alignments. 

Ensure your alginment is in sam format and sorted by name. You can sort your sa files using samtools sort with the -n option.

From the command line, type:

python3 pseudoreplicate_paired_samfile.py [ -r -b -s] -i <file.sam>

-r: number of replicates\
-s: seed sequence\
-b: bam file input

Required python packages:\
numpy \
pysam
