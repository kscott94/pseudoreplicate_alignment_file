# pseudoreplicate_alignment_file
This python script allows you to randomly split a sequence alignment (sam) file into several smaller files, called pseudoreplicates. Paired end reads will be retained within the same file. Also compatible with non-paired alignments. 

Ensure your alginment is in sam format and sorted by name. You can sort your sa files using samtools sort with the -n option.

From the command line, type:

python3 pseudoreplicate_paired_samfile.py -i <file.sam> -r \<number of replicates\>


Required python packages:
numpy \
natsort 7.1.0
