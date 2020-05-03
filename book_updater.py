import requests
import re

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


# read the words of your book
def booktotxt(path):
    document_text = open(path, 'r')  # your source file with a book
    text_string = document_text.read().lower()
    pat = re.findall(r'\b[a-z]{3,25}\b', text_string)
    document_text.close()
    return pat


# find the most frequent words
def frequent(pat, n):
    frequency = {}

    for word in pat:
        count = frequency.get(word, 0)
        frequency[word] = count + 1
    if n > 10:
        lEng = [[k] for k, v in frequency.items() if v > n]
    else:
        lEng = [[k] for k, v in frequency.items() if v < n]
    # allEnglishWords = list(frequency.keys())
    return lEng


# add stars to the English text
def addStars(lEng):
    lEngStar = lEng.copy()
    for i in range(0, len(lEngStar)):
        lEngStar[i] = ', '.join(lEngStar[i]) + ' -*1**'
    return lEngStar


# create chunks of the list of lists
def chunks(text, n):
    for q in range(0, len(text), n):
        yield text[q:q + n]

# go to Yandex to translate words
def request(lists):
    lRusDouble = []
    for list in lists:
        json = lookup(list)
        russianWords = ''.join(json["text"]) + ' -*1**'
        lRusDouble += russianWords.split(' -*1**')

        lRus = []
        for string in lRusDouble:
            if string != "":
                lRus.append(string)
    return lRus


# create flashcards with the words
def flashCards(eng, rus):
    f = open("flashcards.txt", "a")

    for i in range(0, len(lEng)):
        lEngCards = eng.copy()
        lRusCards = rus.copy()
        lEngCards[i] = '"' + ', '.join(lEngCards[i]) + '";'
        lRusCards[i] = '"' + lRusCards[i] + '"'
        tog = (lEngCards[i] + lRusCards[i])
        tog.encode('utf-8').strip()
        # print(tog)
        print(tog, file=f)

    f.close()  # file for language cards creation


def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))

    def translate(match):
        return word_dic[match.group(0)]

    return rc.sub(translate, text)


# updates the book
def updateBook(path, eng, rus):

    for i in range(0, len(eng)):
        eng[i] = ' '.join(eng[i]) + ' '
        rus[i] = eng[i] + '(' + lRus[i] + ') '

    word_list = dict(zip(eng, rus))

    fin = open(path, "r")
    str2 = fin.read()
    fin.close()
    str3 = replace_words(str2, word_list)
    fout = open("updatedBook.txt", "w")
    fout.write(str3)
    fout.close()


bookpath = 'book.txt'

pattern = booktotxt(bookpath)
lEng = frequent(pattern, 900)
lEngStar = addStars(lEng)
print(len(lEng))
list_of_lists = list(chunks(lEngStar, 100))
lRus = request(list_of_lists)
flashCards(lEng, lRus)
updateBook(bookpath, lEng, lRus)






