import requests
import re
import sys
from itertools import islice

# Yandex API
KEY = 'trnsl.1.1.20200501T155620Z.29a16adc41056341.662c3a723031b520e3647e7b0602c6cb5e399214'
URL = "yourYandexTranslateAPIkey"


def translate_me(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()


document_text = open('/Users/user/Desktop/text.txt', 'r') # your source file with a book
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,25}\b', text_string)

frequency = {}

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

limit = 5

my_list = [[k] for k, v in frequency.items() if v < limit]
englishWords = list(frequency.keys())

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

list_of_lists = list(chunks(englishWords, 10)) #10 words at a time, you can change this value

for list in list_of_lists:
          json = translate_me(list)
          print(' '.join(json["text"]))


# diction = {}

# print(len(englishWords))
#
# for i in range(0, len(my_list)):
#     json = translate_me(my_list[i])
#     a = '"'+' '.join(json["text"])+'";'
#     diction['russian'] = a
#     # print(a)
#     b = my_list[i]
#     temp = ""
#     for j in b:
#         if j.isalpha():
#             b = '"'+"".join([temp, j])+'"\n'
#     diction['english'] = b
#     print(b)
#     i += 1
#     s = ''
#     s = (a+b).encode('utf-8').strip()
#     print(s)
#
#     class Logger(object):
#         def __init__(self, filename="Default.log"):
#             self.terminal = sys.stdout
#             self.log = open(filename, "a")
#
#         def write(self, message):
#             self.terminal.write(message)
#             self.log.write(message)
#
#     sys.stdout = Logger("words.txt") # the file is stored in the project directory
#
