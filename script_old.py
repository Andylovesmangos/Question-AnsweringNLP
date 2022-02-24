import csv
import json
import time

from qbmodel import QuizBowlModel

with open('qanta.dev.2018.04.18.json') as f:
    data = json.load(f)
data = data['questions']

questions = [data[i]['text'] for i in range(340, 500)]
pages = [data[i]['page'] for i in range(340, 500)]

right_true = 0
num_true = 0
right_false = 0
num_false = 0

start = time.time()

qb = QuizBowlModel()
gb_list = qb.guess_and_buzz(questions)

for out, page in zip(gb_list, pages):
    if out[1] is True:
        if out[0] == page.replace('_', ' '):
            right_true += 1
        num_true += 1
    else:
        if out[0] != page.replace('_', ' '):
            right_false += 1
        num_false += 1
    print(f'Guess + Buzz: {out}, Answer: {page}')

print('When buzz = True: ')
print(f'# of correct guesses: {right_true}')
print(f'# of total guesses: {num_true}')
print('When buzz = False: ')
print(f'# of incorrect guesses: {right_false}')
print(f'# of total guesses: {num_false}')

end = time.time()
minutes = (end - start) / 60
print(f'# of minutes it took to run: {minutes}')


file = open('guessdev_guesses.csv', 'a')
writer = csv.writer(file)
rows = []
for gb in gb_list:
    rows.append([gb[0], gb[1]])
writer.writerows(rows)
file.close()
