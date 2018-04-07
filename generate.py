import numpy
import argparse
import pickle


def is_service_word(word):
    # It proves that word is BEGIN = None or END = None
    if word is None:
        return True
    return False


parser = argparse.ArgumentParser(description="Hello another one time.", epilog="")
parser.add_argument('--model', required=True, type=str, nargs=1,
                    help="Way with file's name to directory, where file with model is.")
parser.add_argument('--length', type=int, default=[7], help='')
parser.add_argument('--seed', type=str, nargs=1, default=[None], help="First word")
args = parser.parse_args()

# Get dict of collocations and statistic
FILE_IN = open(args.model[0], mode='rb')
STATISTICS = pickle.load(FILE_IN)
if not isinstance(STATISTICS, dict):
    print(type(STATISTICS))
    print('Wrong file!!!')
    exit(1)

# Generate text word by word
word1 = args.seed[0]
if word1 not in STATISTICS.keys():
    print("There is no word '{}'.".format(word1))
    exit(1)

CNT = args.length
if word1 is not None:
    print(word1, end='')
for _ in range(CNT, 1, -1):
    word2 = numpy.random.choice(list(STATISTICS[word1].keys()), 1, list(STATISTICS[word1].values()))[0]
    if is_service_word(word2):
        print('.', end='')
        word1 = word2
        continue
    print(' ', word2, sep='', end='')
    word1 = word2

last_word = numpy.random.choice(list(STATISTICS[word1].keys()), 1, list(STATISTICS[word1].values()))[0]
if is_service_word(last_word):
    print('.', end='')
while is_service_word(last_word):
    last_word = numpy.random.choice(list(STATISTICS[last_word].keys()), 1, list(STATISTICS[last_word].values()))
print(' ', *last_word, sep='')
