import re
import sys
import argparse
import os
import pickle


def update_stat(statistic, parts, statistics):
    # Renew statistic with new words (in list called part)
    for i in range(len(parts) - 1):
        word = parts[i]
        if word not in statistics:
            statistics[word] = 0
        statistics[word] += 1
        next_word = parts[i + 1]
        if word in statistic:
            if next_word not in statistic[word]:
                statistic[word][next_word] = 0
            statistic[word][next_word] += 1
        else:
            statistic[word] = {next_word: 1}


def parse_line(line, parse_all_collocations, parse_frequencies, lc):
    # Split line to sentences and sentences to words
    sentences = [s for s in re.split("\.|!|\?", line) if len(s) > 0]
    for sentence in sentences:
        parse_words = re.sub(r"[^\w]", ' ', sentence)
        if lc:
            parse_words = parse_words.lower()
        words = [BEGIN] + parse_words.split() + [END]
        if len(words) < 3:
            continue
        update_stat(parse_all_collocations, words, parse_frequencies)


def reading(in_directory, all_colloc, freq, lc):
    """
    Read txt-files and count frequencies
    :param in_directory: input directory
    :param all_colloc: dictionary of collocations in text
    :param freq: dictionary of frequencies
    :param lc: if lower case is needed
    :return: dict of collocations and dict of frequencies
    """
    if in_directory is not None:
        in_directory = in_directory[0]
        # Make a list of names of txt-files in input-dir
        try:
            files = os.listdir(in_directory)
        except OSError:
            print("Directory doesn't exist.")
            exit(1)
        txt_files = filter(lambda x: x.endswith('.txt'), files)

        # Read from each file
        exist_txt_files = True
        for filename in txt_files:
            exist_txt_files = False
            fin = open(filename, "r")
            for new_line in fin:
                parse_line(new_line, all_colloc, freq)
        if exist_txt_files:
            print("There're no txt-files in directory.")
            exit(1)
    else:
        # Read from stdin flow
        for new_line in sys.stdin.read():
            parse_line(new_line, all_colloc, freq, lc)

    return all_colloc, freq


def main():
    parser = argparse.ArgumentParser(description="Hi!", epilog="You're nice! Goodbye.")
    parser.add_argument('--input-dir', type=str, nargs=1,
                        help='Way to directory, where your txt-files is, or stdin flow')
    parser.add_argument('--model', required=True, type=str, nargs=1, default='statistics.out',
                        help="Way to file with it's name, where model will be written")
    parser.add_argument('--lc', action="store_true",
                        help="If you want words in lowercase.")
    args = parser.parse_args()

    BEGIN = END = None
    all_collocations = {}
    frequencies = {None: 1}
    lower_case = args.lc
    input_directory = args.input_dir
    all_collocations, frequencies = reading(input_directory, all_collocations,
                                            frequencies, lower_case)

    # Normalize frequencies of collocations
    for word1, dict1 in all_collocations.items():
        frequency = frequencies[word1]
        for word2 in dict1.keys():
            dict1[word2] /= frequency

    # Write dict of collocations in file
    fout = open(args.model[0], mode='wb')
    pickle.dump(all_collocations, fout)
    fout.close()


if __name__ == '__main__':
    main()
