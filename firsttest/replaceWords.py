import re

lEng = ['one', 'two', 'three']
lRus = ['один', 'два', 'три']

for i in range(0, len(lEng)):
    lEng[i] = '' + lEng[i] + ''
    lRus[i] = lEng[i] + ' (' + lRus[i] + ')'


print(lRus)
word_list = dict(zip(lEng, lRus))

with open('book.txt') as main, open('book_upd.txt', 'w') as done:
    text = main.read()
    done.write(re.sub(r'\b\w+\b', lambda x: word_list.get(x.group(), x.group()), text))
