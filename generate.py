import numpy
import argparse
import pickle


def is_service_word(word):
    # It proves that word is '*BEGIN*' or '*END*'
    if word == '*BEGIN*' or word == '*END*':
        return True
    return False


parser = argparse.ArgumentParser(description="Hello another one time.", epilog="")
parser.add_argument('--model', required=True, type=str, nargs=1, default='statistics.out', help='')
parser.add_argument('--seed', type=str, nargs=1, default='', help='')
parser.add_argument('--length', required=True, type=int, nargs=1, default=7, help='')
parser.add_argument('--output', type=str, nargs=1, default='stdout', help='0')
args = parser.parse_args()

FILE_IN = open(args.model[0], mode='rb')
STATISTICS = pickle.load(FILE_IN)
if type(dict()) != type(STATISTICS):
    print('Wrong file!!!')
    exit(0)

"""
for line in FILE_IN.readlines():
    word1, word2, frequency2, frequency1 = line.split()
    frequency = int(frequency2) / int(frequency1)
    if word1 in STATISTICS:
        STATISTICS[word1][0].append(word2)
        STATISTICS[word1][1].append(frequency)
    else:
        STATISTICS[word1] = ([word2], [frequency])
"""

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
