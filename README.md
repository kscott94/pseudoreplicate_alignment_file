# pseudoreplicate_alignment_file
This python script allows you to randomly split a sequence alignment (sam) file into several smaller file, called pseudoreplicates. Paired end reads will be retained within the same file.

From the command line, 
python3 pseudoreplicate_samfile.py -i <file.sam> -r <number of replicates> -s <seed>
