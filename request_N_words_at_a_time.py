import requests
import re

# Yandex API
KEY = 'yourYandexAPIkey'
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"


def lookup(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()


document_text = open('/Users/user/Desktop/text.txt', 'r')  # your source file with a book
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,25}\b', text_string)

frequency = {}

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

lEng = [[k] for k, v in frequency.items() if v > 500]
lEngStar = lEng.copy()
allEnglishWords = list(frequency.keys())
for i in range(0, len(lEngStar)):
    lEngStar[i] = ', '.join(lEngStar[i]) + '-*1**'


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# print(len(lEng))
list_of_lists = list(chunks(lEngStar, 50))

lRusDouble = []



for list in list_of_lists:
    json = lookup(list)
    russianWords = ''.join(json["text"]) + '-*1**'
    lRusDouble += russianWords.split('-*1**')

lRus = []
for string in lRusDouble:
    if string != "":
        lRus.append(string)

        

f = open("output.txt", "a")

for i in range(0, len(lEng)):
    # print(lEng[i])
    lEng[i] = '"' + ', '.join(lEng[i]) + '";'
    lRus[i] = '"' + lRus[i] + '"'
    tog = (lEng[i] + lRus[i])
    tog.encode('utf-8').strip()
    print(tog)
    print(tog, file=f)
    i += 1

f.close()
