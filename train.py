import re
import sys
import argparse
import os
import pickle


def make_stat(statistic, parts, statistics):
    for i in range(len(parts) - 1):
        if len(parts[i]) == 0:
            continue
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


def parse_sentence(line, all_collocations, frequencies):
    sentences = line.split('. ')
    for sentence in sentences:
        parse_words = re.sub(r"[^\w]", ' ', sentence)
        parse_words = parse_words.lower()
        words = [BEGIN] + parse_words.split() + [END]
        if len(words) < 3:
            continue
        make_stat(all_collocations, words, frequencies)


parser = argparse.ArgumentParser(description="Hi!", epilog="You're nice! Goodbye.")
parser.add_argument('--input-dir', type=str, nargs=1, default=['stdin'], help='')
parser.add_argument('--model', required=True, type=str, nargs=1, default='statistics.out', help='')
args = parser.parse_args()

BEGIN = '*BEGIN*'
END = '*END*'
ALL_COLLOCATIONS = {END: {BEGIN: 1}}
FREQUENCIES = {END: 1}

DIR = args.input_dir[0]
if DIR != 'stdin':
    try:
        FILES = os.listdir(DIR)
    except OSError:
        print("Directory doesn't exist.")
        exit(1)

    TXT_FILES = filter(lambda x: x.endswith('.txt'), FILES)

    flag = True
    for filename in TXT_FILES:
        flag = False
        fin = open(filename, "r")
        for new_line in fin.readlines():
            parse_sentence(new_line, ALL_COLLOCATIONS, FREQUENCIES)
    if flag:
        print("There're no txt-files in directory.")
        exit(1)
else:
    lines = sys.stdin.read().split('\n')
    for new_line in lines:
        parse_sentence(new_line, ALL_COLLOCATIONS, FREQUENCIES)

for word1, dict1 in ALL_COLLOCATIONS.items():
    frequency = FREQUENCIES[word1]
    for word2 in dict1.keys():
        dict1[word2] /= frequency

print(ALL_COLLOCATIONS)

FOUT = open(args.model[0], mode='wb')
pickle.dump(ALL_COLLOCATIONS, FOUT)
FOUT.close()

"""
collocations = dict()
for word1, pairs in all_collocations.items():
    for word2, stat in pairs.items():
        print(word1, word2, stat, frequencies[word1], file=FILE_OUT)
"""
