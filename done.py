import pickle

import requests
import re
import fileinput

# Yandex API
KEY = 'key'
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"


def lookup(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()


document_text = open('book.txt', 'r')  # your source file with a book
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,25}\b', text_string)
document_text.close()

frequency = {}

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

lEng = [[k] for k, v in frequency.items() if v > 900]
lEngStar = lEng.copy()
allEnglishWords = list(frequency.keys())
for i in range(0, len(lEngStar)):
    lEngStar[i] = ', '.join(lEngStar[i]) + '-*1**'


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


print(len(lEng))
list_of_lists = list(chunks(lEngStar, 100))

lRusDouble = []

for list in list_of_lists:
    json = lookup(list)
    russianWords = ''.join(json["text"]) + '-*1**'
    lRusDouble += russianWords.split('-*1**')

lRus = []
for string in lRusDouble:
    if string != "":
        lRus.append(string)

f = open("flashcards.txt", "a")

for i in range(0, len(lEng)):
    # print(lEng[i])
    lEngCards = lEng.copy()
    lRusCards = lRus.copy()
    lEngCards[i] = '"' + ', '.join(lEngCards[i]) + '";'
    lRusCards[i] = '"' + lRusCards[i] + '"'
    tog = (lEngCards[i] + lRusCards[i])
    tog.encode('utf-8').strip()
    print(tog)
    print(tog, file=f)

f.close()  # file for language cards creation

for i in range(0, len(lEng)):
    lEng[i] = ' '.join(lEng[i]) + ' '
    lRus[i] = lEng[i] + '(' + lRus[i] + ') '

word_list = dict(zip(lEng, lRus))


# read a text file, replace multiple words specified in a dictionary
# write the modified text back to a file


def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))

    def translate(match):
        return word_dic[match.group(0)]

    return rc.sub(translate, text)


fin = open('book.txt', "r")
str2 = fin.read()
fin.close()

str3 = replace_words(str2, word_list)

fout = open("book_upd.txt", "w")
fout.write(str3)
fout.close()
