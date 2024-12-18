import os,sys
import numpy as np
from dataset.transforms import cropping
from tqdm import tqdm

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_root = os.path.join(root,'data')
dataset_root = os.path.join(root,'dataset')

def Human_Science_2019(args):

    root_feature = os.path.join(dataset_root, args["dataset"],
                                str(args["max_length"]))
    X     = np.load(os.path.join(root_feature, 'X.npy'))
    Y     = np.load(os.path.join(root_feature, 'Y.npy'))
    L     = np.load(os.path.join(root_feature, 'L.npy'))

    return X, Y, L

def Split_Train_Val_Test_Set(X,Y,L,train_index,test_index):
    val_index = np.random.choice(train_index,size=int(0.1*len(train_index)),replace=False)
    train_index_new = np.array([t for t in train_index if t not in val_index])
    X_train, X_val, X_test = X[train_index_new], X[val_index], X[test_index]
    Y_train, Y_val, Y_test = Y[train_index_new], Y[val_index], Y[test_index]
    L_train, L_val, L_test = L[train_index_new], L[val_index], L[test_index]

    return X_train,X_val,X_test,Y_train,Y_val, Y_test,L_train,L_val,L_test


def Split_multi_Train_Val_Test_Set(X,Y,L,
                                    X_CHIP,
                                    train_index,test_index):
    val_index = np.random.choice(train_index, size=int(0.1 * len(train_index)), replace=False)
    train_index_new = np.array([t for t in train_index if t not in val_index])
    X_train, X_val, X_test = X[train_index_new], X[val_index], X[test_index]
    X_CHIP_train, X_CHIP_val, X_CHIP_test = X_CHIP[train_index_new], X_CHIP[val_index], X_CHIP[test_index]
    Y_train, Y_val, Y_test = Y[train_index_new], Y[val_index], Y[test_index]
    L_train, L_val, L_test = L[train_index_new], L[val_index], L[test_index]

    return X_train, X_val, X_test,\
           X_CHIP_train, X_CHIP_val, X_CHIP_test,\
           Y_train, Y_val, Y_test, L_train, L_val, L_test

def data_augmentation(X_train,X_CHIP,Y_train):
    X_train_aug  = []
    Y_train_aug  = []
    X_CHIP_aug   = []
    with tqdm(total=X_train.shape[0]) as t:
        for i in tqdm(range(X_train.shape[0])):
            x = X_train[i]
            y = Y_train[i]
            x_chip = X_CHIP[i]
            len_seq = len(x.nonzero()[0])
            # Original Data
            X_train_aug.append(x)
            X_CHIP_aug.append(x_chip)
            Y_train_aug.append(y)
            # Cropping
            X_train_aug.append(cropping(x, len_seq, random_seed=50))
            X_CHIP_aug.append(x_chip)
            Y_train_aug.append(y)

            # Mirroring & Palindrome
            X_train_aug.append(x[::-1, ::-1])
            X_CHIP_aug.append(x_chip)
            Y_train_aug.append(y)

            t.update()
    # shuffle
    X_train_aug = np.array(X_train_aug)
    Y_train_aug = np.array(Y_train_aug)

    X_CHIP_aug  = np.array(X_CHIP_aug)

    permutation = np.random.permutation(int(X_train_aug.shape[0]))
    shuffled_X = X_train_aug[permutation, :, :]
    shuffled_Y = Y_train_aug[permutation]
    shuffled_X_CHIP_aug   = X_CHIP_aug[permutation,:]
    return shuffled_X,\
           shuffled_X_CHIP_aug,\
           shuffled_Y

def augmentation_func(X_train, Y_train,args):
    X_train_aug = []
    Y_train_aug = []
    with tqdm(total=X_train.shape[0]) as t:
        for x, y in tqdm(zip(X_train, Y_train)):
            len_seq = len(x.nonzero()[0])
            # Original Data
            X_train_aug.append(x)
            Y_train_aug.append(y)
            # Cropping
            X_train_aug.append(cropping(x, len_seq,random_seed=50))
            Y_train_aug.append(y)

            # Mutation
            # X_train_aug.append(mutation(x,len_seq, rate=0.01))
            # Y_train_aug.append(y)

            # Mirroring & Palindrome
            X_train_aug.append(x[::-1, ::-1])
            Y_train_aug.append(y)

            t.update()
    #shuffle
    X_train_aug = np.array(X_train_aug)
    Y_train_aug = np.array(Y_train_aug)
    permutation = np.random.permutation(int(X_train_aug.shape[0]))
    shuffled_X = X_train_aug[permutation, :, :]
    shuffled_Y = Y_train_aug[permutation]

    return shuffled_X , shuffled_Y


if __name__ == '__main__':
    args = {
  "dataset":        "nature_2020",
  "num_data":       4000,
  "max_length":     1000,
  "min_length":     500,
  "model":          "SeqModel_Attention",
  "log_dir":        "logs",
  "output_dir":     "output",
  "output_prefix":  "SeqModel_Attention",

  "input_length":1000,
  "input_height":4,
  "data_augmentation":1,
  "hidden_dim":64,
  "attention":1,
  "equivariant":0,
  "get_distribution":0,
  "get_line_comparison":1,

  "dp_rate":0.1,

  "trails":4,
  "folds":5,
  "epochs":100,
  "batch_size":64,
  "lr":0.001,

  "init_weight":0,
  "reinforce_train":0,
  "loss":"binary_crossentropy"
}

    X,Y,L = Nature_2020(args)
