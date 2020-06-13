import re
import string
import razdel
import pandas as pd


def not_cyrillic(text):
    return bool(re.search(f'[^а-яА-ЯёЁ{string.punctuation}— ]', text))

def filter_bad(row):

    original, paraphrase = row['original'].strip('\n'), row['paraphrase'].strip('\n')

    basic_processing = lambda x: x.lower() \
                                  .replace('ё','е') \
                                  .translate(str.maketrans('', '',
                                             string.punctuation+'—'))

    if any([not_cyrillic(text) or '...' in text 
            for text in [original, paraphrase]]):
        row['original'], row['paraphrase'] = None, None
        return row

    original = [_.text for _ in razdel.tokenize(basic_processing(original))]
    paraphrase = [_.text for _ in razdel.tokenize(basic_processing(paraphrase))]
    n_tokens = [len(original), len(paraphrase)]

    if any([n_tok < 2 or n_tok > 20 for n_tok in n_tokens]) \
        or set(original) == set(paraphrase) \
        or any(len(toks) > 1 and len(set(toks)) == 1
            for toks in [original, paraphrase]):
        row['original'], row['paraphrase'] = None, None
    
    return row