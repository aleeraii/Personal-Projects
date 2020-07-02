from Bio import SeqIO
# ******************** PROBLEM 5 ******************** #
# Write a Python program that, using the genbank record, saves the corresponding protein sequence in fasta format.
gbk = "sequence.gb"                 # storing the genbank file name to a variable
fasta = "converted.fasta"           # saving the name of new file to be created in a variable
input_file = open(gbk, "r")         # opening the genbank file and reading through it
output_file = open(fasta, "w")      # opening the genbank file and writing to it

for seq_record in SeqIO.parse(input_file, "genbank") :             # opening the the genbank file to extract the results
    with open('converted.fasta', 'w') as f:                        # creating new fasta file
        result = '>' + seq_record.description + '\n' + seq_record.seq  # making proper format for the fasta file
        f.write(str(result)+'\n')                                      # writing the sequence to the fasta file

output_file.close()         # closing output fasta file
input_file.close()          # closing input genbank file
print("Genbank File is Converted Into Fasta File")