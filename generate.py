import numpy
import argparse
import pickle


def is_service_word(word):
    # It proves that word is '*BEGIN*' or '*END*'
    if word == '*BEGIN*' or word == '*END*':
        return True
    return False


parser = argparse.ArgumentParser(description="Hello another one time.", epilog="")
parser.add_argument('--model', required=True, type=str, nargs=1,
                    help="Way with file's name to directory, where file with model is.")
parser.add_argument('--length', type=int, nargs=1, default=7, help='')
args = parser.parse_args()

FILE_IN = open(args.model[0], mode='rb')
STATISTICS = pickle.load(FILE_IN)
if type(dict()) != type(STATISTICS):
    print('Wrong file!!!')
    exit(0)

word1 = '*BEGIN*'
CNT = args.length[0]
while CNT > 1:
    word2 = numpy.random.choice(list(STATISTICS[word1].keys()), 1, list(STATISTICS[word1].values()))[0]
    if is_service_word(word2):
        word1 = word2
        continue
    print(word2, end=' ')
    CNT -= 1
    word1 = word2

last_word = numpy.random.choice(list(STATISTICS[word1].keys()), 1, list(STATISTICS[word1].values()))
if is_service_word(last_word):
    word1 = '*BEGIN*'
    print(*numpy.random.choice(list(STATISTICS[word1].keys()), 1, list(STATISTICS[word1].values())))
else:
    print(*last_word)
