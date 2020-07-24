# Implementation of an HMM tagger for part of speech tagging
from collections import Counter, defaultdict
from itertools import chain


from utilities import read_data, read_tags

def pair_counts(sequences_A, sequences_B):
    pair_count = defaultdict(dict)
    sequences_A_flat = [element for sent in sequences_A for element in sent]
    sequences_B_flat = [element for sent in sequences_B for element in sent]
    for tag, word in zip(sequences_A_flat, sequences_B_flat):
        try:
            pair_count[tag][word]=pair_count[tag][word]+1
        except KeyError:
            pair_count[tag][word]=1
    return pair_count


def unigram_counts(sequences):
    sequences_flat = [element for sent in sequences for element in sent]
    return Counter(sequences_flat)


def bigram_counts(sequences):
    bigram_count = {}
    for seq in sequences:
        for idx in range(len(seq)):
            if idx+1 < len(seq):
                if (seq[idx], seq[idx+1]) in bigram_count:
                    bigram_count[(seq[idx], seq[idx+1])]+=1
                else:
                    bigram_count[(seq[idx], seq[idx+1])]=1
    return bigram_count

def starting_counts(sequences):
    tag_starts = {}
    for seq in sequences:
            if seq[0] in tag_starts:
                tag_starts[seq[0]]+=1
            else:
                tag_starts[seq[0]]=1
    return tag_starts


def ending_counts(sequences):
    tag_ends = {}
    for seq in sequences:
            if seq[-1] in tag_ends:
                tag_ends[seq[-1]]+=1
            else:
                tag_ends[seq[-1]]=1
    return tag_ends


tagfile = "tags-universal.txt"
datafile = "brown-universal.txt"

tagset = read_tags(tagfile)
sentences = read_data(datafile)
keys = tuple(sentences.keys())
wordset = frozenset(chain(*[s.words for s in sentences.values()]))
word_sequences = tuple([sentences[k].words for k in keys])
tag_sequences = tuple([sentences[k].tags for k in keys])
N = sum(1 for _ in chain(*(s.words for s in sentences.values())))