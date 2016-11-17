#!/usr/bin/python
"""
I worked with Wen Ya and Gong Haohan.
"""
import sys

#return a tuple:
#   [0] allowed letters
#   [1] matrix(dictionary form)
#   [2] gap
#   [3] list of 2 sequences
#   [4] list of 2 sequence names
def checkinput(arg):
    l = len(arg)
    #check if there are 2 arguments
    if l < 3:
        print("Not enough arguments.")
        return 0
    else:
        #task 1 read scoring matrix
        with open(arg[1]) as score:
            lines = score.readlines()
            #first line, allowed letter
            letters = lines[0]
            letters = letters.strip()
            letters = letters.split(" ")
            matrix = []
            #middle part, aligning scores
            for i in range(1,len(letters)+1):
                m = lines[i].strip().split(" ")
                for j in range(0,len(m)):
                    m[j] = int(m[j])
                matrix.append(m)
            score_dict = {}
            for i in range(len(letters)):
                for j in range(len(letters)):
                    score_dict[letters[i]+letters[j]] = matrix[i][j]
            #last line, gap score
            gap = int(lines[-1].strip())
        #task 2 read fasta
        with open(arg[2]) as seq:
            lines = seq.readlines()
            #check if contain 2 sequences
            sequences = []
            seq_name = []
            for line in lines:
                if line[0] == ">":
                    sequences.append("")
                    seq_name.append(line.strip())
                else:
                    sequences[-1]+=line.strip()
            if len(sequences) != 2:
                print("Sequences error!")
                return 0
        #check if sequences and matrix match each other
        letter_dict = {}
        # record all the allowed letters
        for i in letters:
            letter_dict[i] = 1
        # if letter in the sequence not founded, return 0
        for i in range(0,2):
            for l in sequences[i]:
                if letter_dict[l] == None:
                    return 0
    return (letters,score_dict,gap,sequences,seq_name)
    
if __name__ == '__main__':
    task = checkinput(sys.argv)
    #task = 0 if something goes wrong, else go on processing
    #[0] allowed letters [1] matrix(dictionary) [2] gap [3] list of 2 sequences
    # if task = 0, meaning there are errors and this script will end
    if task:
        gap = task[2]
        seq1 = task[3][0]
        seq2 = task[3][1]
        seq1_len = len(task[3][0])
        seq2_len = len(task[3][1])
        score_dict = task[1]
        #task3 dynamic programming matrix
        #initialize the first column and row
        dp_matrix = [[0 for i in range(seq1_len+1)] for j in range(seq2_len+1)]
        for i in range(1,seq1_len+1):
            dp_matrix[0][i] = dp_matrix[0][i-1]+gap
        for i in range(1,seq2_len+1):
            dp_matrix[i][0] = dp_matrix[i-1][0]+gap
        #calculate the matrix
        for i in range(1,seq2_len+1):
            for j in range(1,seq1_len+1):
                pair = seq1[j-1]+seq2[i-1]
                dp_matrix[i][j] = max(dp_matrix[i-1][j-1]+score_dict[pair],\
                                    dp_matrix[i-1][j]+gap,\
                                    dp_matrix[i][j-1]+gap)
        #output the matrix
        for i in dp_matrix:
            i = [str(a) for a in i]
            i = ' '.join(i)
            print(i)
        
        
        #task 4 trace back
        #start from right bottom
        col = seq1_len
        row = seq2_len
        
        seq1_align = ""
        seq2_align = ""
            
        while(col > 0 or row > 0):
            pair = seq1[col-1]+seq2[row-1]
            # check where this score is from
            # from up left
            if dp_matrix[row][col] == dp_matrix[row-1][col-1]+score_dict[pair]:
                seq1_align += seq1[col-1]
                seq2_align += seq2[row-1]
                row -= 1
                col -= 1
            # from up
            elif dp_matrix[row][col] == dp_matrix[row-1][col]+gap:
                seq1_align += "-"
                seq2_align += seq2[row-1]
                row -= 1
            # from left
            elif dp_matrix[row][col] == dp_matrix[row][col-1]+gap:
                seq1_align += seq1[col-1]
                seq2_align += "-"
                col -= 1
            
        # reverse the string
        seq1_align = seq1_align[::-1]
        seq2_align = seq2_align[::-1]
        # output the alignment
        print(task[4][0])
        print(seq1_align)
        print(task[4][1])
        print(seq2_align)
