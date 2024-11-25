import numpy as np
import random
one_hot_conv = {"A": [1, 0, 0, 0], "T": [0, 0, 0, 1],
                "C": [0, 1, 0, 0], "G": [0, 0, 1, 0],
                "a": [1, 0, 0, 0], "t": [0, 0, 0, 1],
                "c": [0, 1, 0, 0], "g": [0, 0, 1, 0],
                "n": [0, 0, 0, 0], "N": [0, 0, 0, 0]}
capital ={"A": "A", "T": "T",
          "C": "C", "G": "G",
          "a": "A", "t": "T",
          "c": "C", "g": "G"}
from scipy import signal

def cropping(inpt,len_seq,random_seed):
    out = np.zeros(inpt.shape)
    end_idx = random.randint(len_seq-random_seed, len_seq)
    out[0:end_idx,:] = inpt[0:end_idx,:]
    return out

mutation_dic = {
    "1":[1,0,0,0],
    "2":[0,1,0,0],
    "3":[0,0,1,0],
    "4":[0,0,0,1]
}
