#stdlib includes
import argparse
import csv
import glob
import os

from itertools import repeat
import concurrent.futures

# external includes
import numpy as np
import scipy.io as sio

#internal includes
import stemmer
import process_email
import svm

def load_vocab(fname):
    with open(fname) as vocab:
        return {row['word']: int(row['index'])-1 for row in csv.DictReader(vocab, delimiter='\t')}

# pool.map only allows one iterable, so I pack both into a tuple
def file_to_word_vec(fname, vocab):
    # The files in the provided link have invalid unicode sequences
    with open(fname, errors='ignore') as email:
        return_arr = np.zeros(len(vocab))
        words = process_email.process_email(email.read())
        for word in words:
            if word in vocab:
                return_arr[vocab[word]]=1
    return return_arr


def split_train(vectors, percent):
    shuffle = np.random.permutation(len(vectors))

    vectors = vectors[shuffle]
    len_to_take = int(len(vectors) * percent);
    return vectors[:len_to_take], vectors[len_to_take:]

def prepare_vectors(email_dir, percent, vocab):
    files = glob.glob(email_dir + '/*')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        vectors = list(executor.map(file_to_word_vec, files, repeat(vocab)))
    return split_train(np.stack(vectors), percent)

def run_report(data, seed, train, weight, use_download):
    np.random.seed(seed)

    if use_download:
        vocab_file = os.path.join(data, 'vocab.txt')
        with open(vocab_file) as vf:
            vocab = load_vocab(vocab_file)

        ham_dir = os.path.join(data, 'email_data', 'ham')
        spam_dir = os.path.join(data, 'email_data', 'spam')

        ham_train, ham_test = prepare_vectors(ham_dir, train, vocab)
        spam_train, spam_test = prepare_vectors(spam_dir, train, vocab)

    else:
        mat_test = sio.loadmat(os.path.join(data, 'spamTest.mat'))
        mat_train = sio.loadmat(os.path.join('spamTrain.mat'))

        train_x = mat_train['X']
        train_y = mat_train['y'].reshape(len(train_x))

        test_x = mat_test['Xtest']
        test_y = mat_test['ytest'].reshape(len(test_x))

        ham_train = train_x[train_y == 1]
        spam_train = train_x[train_y == 0]

        ham_test = test_x[test_y == 1]
        spam_test = test_x[test_y == 0]

    weight, off = svm.train_linear_svm(ham_train, spam_train, weight)

    ham_score = svm.score_svm(ham_test, np.ones(len(ham_test)), weight, off)
    spam_score = svm.score_svm(spam_test, -1*np.ones(len(spam_test)), weight, off)
    total_score = (ham_score * len(ham_test) + spam_score * len(spam_test)) / (len(ham_test) + len(spam_test))
    return ham_score, spam_score, total_score

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run final report for svm classifier',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--data", help="Location of the data directory",
                        required=True)
    parser.add_argument("--seed", help="RNG seed to ensure replicability", type=int,
                         default=0xDEAD111F)
    parser.add_argument("--train", type=float, help="Portion of data to use as training",
                        required=True)
    parser.add_argument("--weight", type=float, help="Bias svm towards classifying spam correctly",
                        default=0.5)
    parser.add_argument("--use-download", action='store_true',
                        help="Uses downloaded email dataset instead of provided samples")


    args = parser.parse_args()

    if args.train <= 0 or args.train >= 1:
        parser.error("Training portion is {}, must be between zero and one".format(args.weight))

    if args.weight <= 0 or args.weight >= 1:
        parser.error("Spam weight is {}, must be between zero and one".format(args.weight))

    ham, spam, total = run_report(args.data, args.seed, args.train, args.weight, args.use_download)

    print("Score on ham is ", ham)
    print("Score on spam is ", spam)
    print("Sore overall is", total)

