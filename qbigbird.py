from collections import Counter
import ssl

import nltk
from nltk.tokenize import sent_tokenize
import torch
from transformers import pipeline
import wikipedia as wiki

from utils import (
    clean_last_sent,
    add_proper_tail,
    get_nnp_query,
    get_nn_query,
    get_wiki_text,
    get_text_chunks,
    filter_answers,
)


class QBigBird:

    def __init__(
            self,
            model='valhalla/electra-base-discriminator-finetuned_squadv1',
            max_context_length=512,
            top_n=5,
            buzz_threshold=0.3
    ):
        device = 0 if torch.cuda.is_available() else -1
        self.qa = pipeline('question-answering', model=model, device=device)
        self.max_context_length = max_context_length
        self.top_n = top_n

        # necessary downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    def guess_and_buzz(self, question):
        # get last sentence of question, clean and improve it
        text = sent_tokenize(question)[-1]
        text = clean_last_sent(text)
        text = add_proper_tail(text)

        query = get_nnp_query(question)
        query_words = query.split()
        # if not enough proper nouns, try using nouns
        if len(query_words) < 2:
            return 'not enough pns', False
            '''
            query = get_nn_query(text)
            query_words = query.split()

            if len(query_words) < 2:
                return 'not enough nouns', False
            '''

        wikitext = get_wiki_text(query)
        if wikitext == 'PageError :/':
            return wikitext, False

        answer_set = set()
        text_chunks = get_text_chunks(wikitext, self.max_context_length)
        for chunk in text_chunks:

            if any(word in chunk for word in query_words):

                result = self.qa({'question': text, 'context': chunk})
                answer = result['answer']
                score = result['score']
                answer_set.add((answer, score))

        answer_set = filter_answers(answer_set, question)
        if len(answer_set) == 0:
            return ' ', False

        answers_scores = list(answer_set)
        top_answers_scores = sorted(answers_scores, key=lambda tup: tup[1], reverse=True)[:self.top_n]
        # print(f'Top answers: {top_answers_scores}')
        if top_answers_scores[0][1] < 0.01:
            return top_answers_scores[0][0], False

        answer_freq = Counter(answer for answer, score in top_answers_scores)
        freq_top_answers_scores = sorted(top_answers_scores, key=lambda tup: (answer_freq[tup[0]], tup[1]), reverse=True)
        freq_top_answer = freq_top_answers_scores[0][0]
        # get the exact Wikipedia title
        freq_top_answer = wiki.search(freq_top_answer)[0]

        print("Score: ", freq_top_answers_scores[0][1])

        if freq_top_answers_scores[0][1] >= 0.5:
            buzz = True
        else:
            buzz = False

        return freq_top_answer, buzz
