from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re
import wikipedia as wiki


# cleans last sentence of Quiz Bowl question
def clean_last_sent(text):
    cleaned = text.replace('FTP,', 'For 10 points,')
    cleaned = re.sub('(?i)for 10 points,', '', cleaned)

    return cleaned


# gives the question a more "question-like" ending if the question hasn't reached the last sentence yet
def add_proper_tail(text):
    if 'name this' in text.lower() or 'this' not in text.lower():
        return text

    if text[-1] == '.':
        beginning = ' name this '
    else:
        beginning = '. name this '
    words = text.split()
    words = [word.lower() for word in words]
    idx_of_this = words.index('this')
    tail = beginning + words[idx_of_this + 1] + '.'
    new_text = text + tail

    return new_text


# gets valid query using proper nouns in reverse order
def get_nnp_query(text):
    # take out words in quotes
    text = re.sub('"(.*?)"', '', text)

    # find all proper nouns
    tagged_sent = pos_tag(word_tokenize(text))
    proper_nouns = [word for word, pos in tagged_sent if 'NNP' in pos]
    proper_nouns.reverse()

    query = ''
    for nnp in proper_nouns:

        test_query = query + nnp
        results = wiki.search(test_query)
        if len(results) == 0:
            continue
        query += nnp + ' '

    return query


# gets valid query using nouns in reverse order
def get_nn_query(text):
    # take out words in quotes
    text = re.sub('"(.*?)"', '', text)

    # find all types of nouns
    tagged_sent = pos_tag(word_tokenize(text))
    nouns = [word for word, pos in tagged_sent if 'NN' in pos]
    nouns.reverse()

    query = ''
    for nn in nouns:
        test_query = query + nn
        results = wiki.search(test_query)
        if len(results) == 0:
            continue
        query += nn + ' '

    return query


# helper func to allow use of lambda in map
def lower(string):
    return string.lower()


# checks if either of the texts are subsets of the other
def is_either_text_subset(text1, text2):
    # tokenize words, lower() them, and get the unique words in a set
    text1_set = set(map(lambda word: lower(word), word_tokenize(text1)))
    text2_set = set(map(lambda word: lower(word), word_tokenize(text2)))

    if text1_set.issubset(text2_set) or text2_set.issubset(text1_set):
        return True

    return False


# checks if the text is a wikipedia page
def has_wiki_page(text):
    results = wiki.search(text)
    if not results:
        return False

    title = results[0]
    if text.lower() == title.lower():
        return True

    return False


# uses the 3 functions above to filter the answer set
def filter_answers(set_, text):
    # make sure the answers are more than two characters to avoid random letter(s) which sometime appear
    set_ = {tup for tup in set_ if len(tup[0]) > 2}
    # make sure the answers are not in the question
    set_ = {tup for tup in set_ if not is_either_text_subset(tup[0], text)}
    # make sure the all answers have their own Wikipedia pages
    set_ = {tup for tup in set_ if has_wiki_page(tup[0])}
    return set_


# gets the text of the first result of the given query in a Wikipedia search
def get_wiki_text(query):
    results = wiki.search(query)
    # print(results)
    try:
        top_page = wiki.page(results[0])
        # print(result)
    except:
        return 'PageError :/'
    text = top_page.content
    return text


# splits the text into "chunks" of the requested size
def get_text_chunks(text, size):
    splits = []
    for i in range(0, len(text), size):
        splits.append(text[i: i + size])

    return splits
