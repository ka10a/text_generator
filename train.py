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
lc = args.lc

# Read txt-files and count frequencies
input_directory = args.input_dir
if input_directory is not None:
    input_directory = input_directory[0]
    # Make a list of names of txt-files in input-dir
    try:
        FILES = os.listdir(input_directory)
    except OSError:
        print("Directory doesn't exist.")
        exit(1)
    TXT_FILES = filter(lambda x: x.endswith('.txt'), FILES)

    # Read from each file
    exist_txt_files = True
    for filename in TXT_FILES:
        exist_txt_files = False
        fin = open(filename, "r")
        for new_line in fin.readlines():
            parse_line(new_line, all_collocations, frequencies)
    if exist_txt_files:
        print("There're no txt-files in directory.")
        exit(1)
else:
    # Read from stdin flow
    lines = sys.stdin.read().split('\n')
    for new_line in lines:
        parse_line(new_line, all_collocations, frequencies, lc)

# Normalize frequencies of collocations
for word1, dict1 in all_collocations.items():
    frequency = frequencies[word1]
    for word2 in dict1.keys():
        dict1[word2] /= frequency

# Write dict of collocations in file
fout = open(args.model[0], mode='wb')
pickle.dump(all_collocations, fout)
fout.close()
