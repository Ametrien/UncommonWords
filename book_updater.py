import requests
import re
import csv

# Yandex API
KEY = 'key'
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"


bookPath = 'book.txt'
csv1 = 'some.csv'
csv2 = 'some2.csv'


def lookup(mytext):
    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'en-ru'
    }
    response = requests.get(URL, params=params)
    return response.json()


# read the words of your book
def textExctractorLower(path):
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
    if n > 25:
        eng = [[k] for k, v in frequency.items() if v > n]
    else:
        eng = [[k] for k, v in frequency.items() if v < n]

    flat = []
    for sublist in eng:
        for item in sublist:
            flat.append(item)
    # allEnglishWords = list(frequency.keys())

    return flat


# add stars to the English text
def addStars(eng):
    lEngStar = eng.copy()
    lEngStar = [s + '-*1**' for s in lEngStar]

    return lEngStar


# create chunks of the list of lists
def chunks(text, n):
    for q in range(0, len(text), n):
        yield text[q:q + n]


# go to Yandex to translate words
def request(eng):

    engStar = addStars(eng)
    lists = chunks(engStar, 100)

    lRusDouble = []
    for list in lists:
        json = lookup(list)
        russianWords = ''.join(json["text"]) + '-*1**'
        lRusDouble += russianWords.split('-*1**')

        lRus = []
        for string in lRusDouble:
            if string != "":
                lRus.append(string)
    return lRus


# create flashcards with the words
def flashCards(eng, rus):
    f = open("flashcards.txt", "a")

    for i in range(0, len(eng)):
        lEngCards = eng.copy()
        lRusCards = rus.copy()
        lEngCards = ['"' + s + '";' for s in lEngCards]
        # lEngCards[i] = '"' + ', '.join(lEngCards[i]) + '";'
        lRusCards = ['"' + s + '"' for s in lRusCards]
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

    lRus4list = rus.copy()
    lEng4list = eng.copy()

    for i in range(0, len(eng)):
        lEng4list[i] = ''.join(eng[i]) + ' '
        lRus4list[i] = lEng4list[i] + '(' + lRus4list[i] + ') '

    word_list = dict(zip(lEng4list, lRus4list))

    fin = open(path, "r")
    str2 = fin.read()
    fin.close()

    str3 = replace_words(str2, word_list)
    fout = open("updatedBook.txt", "w")
    fout.write(str3)
    fout.close()

def to_csv(eng, rus, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(eng, rus))


def row_from_csv(read, n):
    with open(read, 'r') as f:
        reader = csv.reader(f)
        i = 0
        lang = []
        for row in reader:
            lang.append(row[n])  # do not forget to start with 0
            i += 1
        # print(lang)
        return lang


def from_csv(read, eng, rus):
    eng = row_from_csv(read, 0)
    rus = row_from_csv(read, 1)
    # print(eng)
    # print(rus)
    return eng, rus


def assign():
    lEng2 = []
    lRus2 = []

    eng, rus = from_csv(csv1, lEng2, lRus2)
    lEng2.extend(eng)
    lRus2.extend(rus)
    print(lEng2)
    print(lRus2)


def requestAndRun():
    allWords = textExctractorLower(bookPath)
    lEng = frequent(allWords, 6)
    lRus = request(lEng)
    flashCards(lEng, lRus)
    updateBook(bookPath, lEng, lRus)
    to_csv(lEng, lRus, csv1)
    assign()

    
def csvAndRun():
    lEng = []
    lRus = []
    from_csv('edited.csv', lEng, lRus)
    assign()
    updateBook('book.txt', lEng, lRus)

    
requestAndRun()


