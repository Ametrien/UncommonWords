import requests
import re
import sys

document_text = open('/Users/username/Desktop/text.txt', 'r') # your source file with a book
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,25}\b', text_string)

frequency = {}

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

limit = 900

my_list = [[k] for k, v in frequency.items() if v > limit]
my_list.sort(reverse=True)

# Yandex API
KEY = 'yourYandexTranslateAPIkey'
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"


def translate_me(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()

diction = {}

print(len(my_list))

for i in range(0, len(my_list)):
    json = translate_me(my_list[i])
    a = '"'+' '.join(json["text"])+'";'
    diction['russian'] = a
    # print(a)
    b = my_list[i]
    temp = ""
    for j in b:
        if j.isalpha():
            b = '"'+"".join([temp, j])+'"\n'
    diction['english'] = b
    # print(b)
    i += 1
    s = ''
    s = (a+b).encode('utf-8').strip()
    print(s) #outputs the string in the format of Reword mobile app for learning words with the help of cards


    class Logger(object):
        def __init__(self, filename="Default.log"):
            self.terminal = sys.stdout
            self.log = open(filename, "a")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

    sys.stdout = Logger("new_words.txt") # the file is stored in the project directory
