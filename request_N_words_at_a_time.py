import requests
import re
import sys

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger("words.txt")  # the file is stored in the project directory


# Yandex API
KEY = 'yourYandexKey'
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"

def translate_me(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()


document_text = open('/Users/username/Desktop/text.txt', 'r')  # your source file with a book
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,25}\b', text_string)

frequency = {}

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

lEng = [[k] for k, v in frequency.items() if v > 900]
allEnglishWords = list(frequency.keys())


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

print(len(lEng))
list_of_lists = list(chunks(lEng, 30))

s = ''

for list in list_of_lists:
    json = translate_me(list)
    russianWords = ' '.join(json["text"]) + ' '
    s += russianWords
    lRus = s.split()

# for j in range(0, len(lRus)):
#     print(lRus[j]).encode('utf-8').strip()

for i in range(0, len(lEng)):
    # print(lEng[i])
    lEng[i] = '"' + ', '.join(lEng[i]) + '";'
    lRus[i] = '"' + lRus[i] + '";'
    tog = ''
    tog = lEng[i] + lRus[i]
    print(tog).encode('utf-8').strip()
    i += 1

