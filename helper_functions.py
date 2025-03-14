import pandas as pd
from tqdm import tqdm
from collections import Counter

from scipy.stats import mannwhitneyu
from scipy.stats.mstats import kruskal


__all__ = ["tokenize", "words_count", "drop_uncommon_words", "pattern_counts", "update_exact_match",
           "count_to_dataframe", "total_counts"]


def tokenize(sentence, model, punctuations, stop_words):
    sentence = model(sentence)
    # Lemmatize
    sentence = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in sentence]
    # Remove stop words
    sentence = [word for word in sentence if word not in stop_words and word not in punctuations]
    return sentence


def words_count(sequences, counter, model, punctuations, stop_words):
    for sentence in tqdm(sequences):
        counter.update(tokenize(sentence.strip(), model, punctuations, stop_words))
    return counter


def drop_uncommon_words(threshold=5, counter=None):
    for k, v in counter.copy().items():
        if len(k) <= 1:
            del counter[k]
        elif v < threshold:
            del counter[k]
    return counter


def pattern_counts(counter, pattern='bard', update_key='none'):
    total = 0
    drop = []
    for k, v in counter.items():
        if pattern in k and k != pattern and k:
            total += v
            drop.append(k)
    for k in drop:
        del counter[k]
    counter[update_key] += total

    return counter


def update_exact_match(counter, match='gpt', update_key=None):
    if counter[match]:
        counter[update_key] += counter[match]
        del counter[match]
    return counter


def count_to_dataframe(count):
    df = pd.DataFrame.from_dict(count, orient='index').reset_index()
    df.columns = ['Words', 'Frequency']
    df = df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)

    return df


def total_counts(sequences, model, punctuations, stop_words, threshold, patterns=None,
                 update_keys=None, matches=None, matches_keys=None):
    assert len(matches_keys) == len(matches)
    assert isinstance(matches_keys, list) and isinstance(matches, list)
    assert len(patterns) == len(update_keys)
    assert isinstance(patterns, list) and isinstance(matches, list)

    counter = Counter()
    counter = words_count(sequences, counter, model, punctuations, stop_words)
    for p, k in zip(patterns, update_keys):
        counter = pattern_counts(counter, p, k)

    counter = drop_uncommon_words(threshold, counter)

    for m, mk in zip(matches, matches_keys):
        counter = update_exact_match(counter, m, mk)

    return count_to_dataframe(counter)


def significance_scoring(data: iter, stat: str = 'kruskal'):

    assert stat in ['kruskal', 'mann-whitney']

    if stat == 'kruskal':
        h, p = kruskal(*data)

    else:
        h, p = mannwhitneyu(*data)

    if p < 0.05:
        print(f'Accept the alternative hypothesis p-value: {p:.3}')
    else:
        print(f'Fail to reject the null hypothesis p-value: {p:.3}')

    return h, p