import os
import random
import json

def is_end(word):
    return word[-1] in ['.', '!', '?']

def get_stats(text="And this and that."):
    procesed_words = text.split()
    stats = {}

    for i in range(len(procesed_words) - 1):
        if procesed_words[i] in stats.keys():
            stats[procesed_words[i]].append(procesed_words[i+1])
        else:
            stats[procesed_words[i]] = [procesed_words[i+1]]

    return stats

def add_to_stats(stats, text=""):
    if stats is None:
        return get_stats(text)
    procesed_words = text.split()

    for i in range(len(procesed_words) - 1):
        if procesed_words[i] in stats.keys():
            stats[procesed_words[i]].append(procesed_words[i+1])
        else:
            stats[procesed_words[i]] = [procesed_words[i+1]]
    return stats

    return stats

def babble(stats, sentences):
    result = ""
    for _ in range(sentences):
        try:
            word = random.choice(list(stats.keys()))
            sentence = word.capitalize()
            while not is_end(word):
                word = random.choice(stats[word])
                sentence += " " + word
            result += sentence + " "
        except (KeyError, IndexError):
            continue
    return result.strip()