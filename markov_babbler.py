import os
import random
import json
import dropbox

DROPBOX_KEY = os.getenv('DROPBOX_KEY')
if DROPBOX_KEY is None:
    raise ValueError('Environment variable "DROPBOX_KEY" not set.')
dbx = dropbox.Dropbox(DROPBOX_KEY)

def is_end(word):
    return word[-1] in ['.', '!', '?']

def get_stats(text, stats = {}):
    """ Provides stats of a text in the form: {word : {word that follows it : number of times that word has followed it}} """
    # Now replaces add_to_stats()
    procesed_words = text.split()

    for i in range(len(procesed_words) - 1):
        if procesed_words[i] in stats.keys():
            if procesed_words[i+1] in stats[procesed_words[i]].keys():
                stats[procesed_words[i]][procesed_words[i+1]] += 1
            else:
                stats[procesed_words[i]][procesed_words[i+1]] = 1
        else:
            stats[procesed_words[i]] = {procesed_words[i+1] : 1}

    return stats

def babble(stats, sentences):
    """ Generates text based on stats provided in the format: {word : {word that follows it : number of times that word has followed it}} """
    result = ""
    for _ in range(sentences):
        try:
            word = random.choice(list(stats.keys()))
            sentence = word.capitalize()
            while not is_end(word):
                word = random.choices(list(stats[word].keys()), weights=list(stats[word].values()), k=1)[0]
                sentence += " " + word
            result += sentence + " "
        except (KeyError, IndexError):
            continue
    return result.strip()

def get_cloud_stats():
    try:
        metadata, res = dbx.files_download("/lilguys-markov/stats.json")
        data = res.content
        
        stats = json.loads(data.decode('utf-8'))
        return stats
    except Exception as e:
        return {}

def save_cloud_stats(stats):
    stats_str = json.dumps(stats)
    stats_bytes = stats_str.encode('utf-8')
    dbx.files_upload(stats_bytes, '/lilguys-markov/stats.json', mode=dropbox.files.WriteMode.overwrite)