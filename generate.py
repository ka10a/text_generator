import numpy
import argparse
import pickle


def is_service_word(word):
    # It proves that word is BEGIN = None or END = None
    return word is None


def read_stat(arguments):
    # Generate text word by word
    # Get dict of collocations and statistic
    file_in = open(arguments.model[0], mode='rb')
    stat = pickle.load(file_in)

    if not isinstance(stat, dict):
        print("Wrong file!!! Your file's type isn't dict.")
        exit(1)

    return stat


def main():
    parser = argparse.ArgumentParser(description="Hello another one time.", epilog="")
    parser.add_argument('--model', required=True, type=str, nargs=1,
                        help="Way with file's name to directory, where file with model is.")
    parser.add_argument('--length', type=int, default=10, help='Length of text what you want.')
    parser.add_argument('--seed', type=str, nargs=1, default=[None], help="First word")
    args = parser.parse_args()


    statistics = read_stat(args)
    word1 = args.seed[0]
    if word1 not in statistics.keys():
        print("There is no word '{}'.".format(word1))
        exit(1)

    CNT = args.length
    if word1 is not None:
        print(word1, end='')
    for _ in range(CNT, 1, -1):
        word2 = numpy.random.choice(list(statistics[word1].keys()), 1, list(statistics[word1].values()))[0]
        if is_service_word(word2):
            print('.', end='')
            word1 = word2
            continue
        print(' ', word2, sep='', end='')
        word1 = word2

    last_word = numpy.random.choice(list(statistics[word1].keys()), 1, list(statistics[word1].values()))[0]
    if is_service_word(last_word):
        print('.', end='')
    while is_service_word(last_word):
        last_word = numpy.random.choice(list(statistics[last_word].keys()), 1, list(statistics[last_word].values()))
    print(' ', *last_word, sep='')


if __name__ == '__main__':
    main()
