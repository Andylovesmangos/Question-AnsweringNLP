import csv
import json
import time

from qbigbird import QBigBird

with open('qanta.dev.2018.04.18.json') as f:
    data = json.load(f)
data = data['questions']

questions = [data[i]['text'] for i in range(775, len(data))]
pages = [data[i]['page'] for i in range(775, len(data))]

right_true = 0
num_true = 0
right_false = 0
num_false = 0

start = time.time()

qbb = QBigBird()

# guess,buzz
file1 = open('guessdev_guesses.csv', 'a')
writer1 = csv.writer(file1)

# guess,buzz,answer
#file2 = open('error_analysis.csv', 'a')
#writer2 = csv.writer(file2)

for i in range(len(questions)):
    try:
        guess, buzz = qbb.guess_and_buzz(questions[i])
    except:
        guess, buzz = ' ', False

    if buzz is True:
        if guess == pages[i].replace('_', ' '):
            right_true += 1
        num_true += 1
    else:
        if guess != pages[i].replace('_', ' '):
            right_false += 1
        num_false += 1

    try:
        writer1.writerow([guess, buzz])
    except:
        writer1.writerow([' ', False])

    #writer2.writerow([guess, buzz, pages[i]])
    print(f'{i+775} - Guess + Buzz: {guess}, {buzz}, Answer: {pages[i]}')

file1.close()
#file2.close()

print('When buzz = True: ')
print(f'# of correct guesses: {right_true}')
print(f'# of total guesses: {num_true}')
print('When buzz = False: ')
print(f'# of incorrect guesses: {right_false}')
print(f'# of total guesses: {num_false}')

end = time.time()
minutes = (end - start) / 60
print(f'# of minutes it took to run: {minutes}')