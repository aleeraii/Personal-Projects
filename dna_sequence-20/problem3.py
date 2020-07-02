from Bio import SeqIO

# ******************** PROBLEM 3 ******************** #
# Write a Python program that takes the sequences.fasta file and writes N single-sequence
# FASTA files, called sequence{number}.fasta, each one containing a single sequence of the original file.

i = 0  # using this variable for naming the result files in a proper sequence
for seq_record in SeqIO.parse("sequence.fasta", "fasta"):  # opening the the fasta file to extract the results
    with open('sequence-%s.fasta' % str(i), 'w') as f:     # creating new fasta file which stores one sequence only
        f.write(str(seq_record.seq))                       # writing extracted sequence to the new created fasta file
        i += 1                                             # increasing the value so that next file name is changed
print('N Single Sequence Files Generated ')