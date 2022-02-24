from typing import List, Tuple
import random

from qbigbird import QBigBird


class QuizBowlModel:

    def __init__(self):
        """
        Load your model(s) and whatever else you need in this function.
        Do NOT load your model or resources in the guess_and_buzz() function,
        as it will increase latency severely.
        """
        self.model = QBigBird()

    def guess_and_buzz(self, question_text: List[str]) -> List[Tuple[str, bool]]:
        """
        This function accepts a list of question strings, and returns a list of tuples containing
        strings representing the guess and corresponding booleans representing
        whether or not to buzz.
        So, guess_and_buzz(["This is a question"]) should return [("answer", False)]
        If you are using a deep learning model, try to use batched prediction instead of
        iterating using a for loop.
        """
        guess_buzz_list = []
        for i in range(len(question_text)):
            '''
            # only tries to answer ~10% of the questions properly
            if random.random() > 0.1:
                guess_buzz_list.append(('', False))
                continue
            '''
            
            try:
                guess, buzz = self.model.guess_and_buzz(question_text[i])
            except:
                guess, buzz = ' ', False
            
            guess_buzz_list.append((guess, buzz))

        return guess_buzz_list
