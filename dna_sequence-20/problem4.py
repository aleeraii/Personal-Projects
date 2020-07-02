from Bio import SeqIO
from Bio.Seq import Seq
# ******************** PROBLEM 4 ******************** #
# Write a Python program that takes the sequences.fasta file and writes a revcomp.fasta
# file with the reverse complements of the original sequences.


for seq_record in SeqIO.parse("sequence.fasta", "fasta"):   # opening the the fasta file to extract the results
    with open('revcomp.fasta', 'a') as f:                   # creating new fasta file which stores complement
        seq = str(seq_record.seq)                           # getting the sequence and converting into string
        dna = Seq(seq)                                      # making the string a proper sequence
        comp = dna.reverse_complement()                     # finding the reverse complement using built in function
        result = '>'+seq_record.description+'\n'+comp       # generating the proper format for fasta file
        f.write(str(result)+'\n')                           # writing compliment to newly created file
print("File With The Reverse Compliment is Generated")