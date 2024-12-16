# pseudoreplicate BAM file
This python script allows you to randomly subsample a sequence alignment file (bam or sam format) into several smaller files, called pseudoreplicates. Paired-end reads will always be retained within the same file. Also compatible with non-paired alignments. 

Ensure your alginment is in sam format and sorted by name. You can sort your bam files using samtools sort while envoking the -n flag.

### Usage: 
From the command line, type:

python3 pseudoreplicate_paired_samfile.py [ -r -b -s] -i <file.sam>

-r: number of pseudoreplicates\
-s: seed sequence\
-b: bam file input

### Required python packages:
numpy \
pysam
