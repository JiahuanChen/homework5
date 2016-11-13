# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:05:48 2016

@author: blowv6
"""
import sys

#return a tuple:
#   [0] allowed letters
#   [1] matrix(dictionary form)
#   [2] gap
#   [3] list of 2 sequences
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
            for line in lines:
                if line[0] == ">":
                    sequences.append("")
                else:
                    sequences[-1]+=line.strip()
            if len(sequences) != 2:
                print("Sequences error!")
                return 0
    return (letters,score_dict,gap,sequences)
    
if __name__ == '__main__':
    task = checkinput(sys.argv)
    #task = 0 if something goes wrong, else go on processing
    #[0] allowed letters [1] matrix(dictionary) [2] gap [3] list of 2 sequences
    if task:
        gap = task[2]
        seq1 = task[3][0]
        seq2 = task[3][1]
        seq1_len = len(task[3][0])
        seq2_len = len(task[3][1])
        score_dict = task[1]
        #task3 dynamic programming matrix
        dp_matrix = [[0 for i in range(seq1_len+1)] for j in range(seq2_len+1)]
        for i in range(1,seq1_len+1):
            dp_matrix[0][i] = dp_matrix[0][i-1]+gap
        for i in range(1,seq2_len+1):
            dp_matrix[i][0] = dp_matrix[i-1][0]+gap
        for i in range(1,seq2_len+1):
            for j in range(1,seq1_len+1):
                pair = seq1[j-1]+seq2[i-1]
                dp_matrix[i][j] = max(dp_matrix[i-1][j-1]+score_dict[pair],\
                                    dp_matrix[i-1][j]+gap,\
                                    dp_matrix[i][j-1]+gap)
        for i in dp_matrix:
            i = [str(a) for a in i]
            i = ' '.join(i)
            print(i)