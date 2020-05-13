"""
    Author:    Jaineel Vyas
    Filename:   predict.py
"""

import DecisionT as dt

import Adaboost as ada


import pickle


def englishverb(line):

    verbs = ('leave', 'kepp', 'come', 'ask', 'look', 'live', 'run', 'walk', 'run', 'play', 'turn', 'try', 'work', 'say'
             , 'make', 'give', 'hear', 'give', 'may', 'find')
    words = line.split(" ")

    for word in words:
        if any(w in verbs for w in word.lower()):
            return 'True'

    return 'False'


def dutchverbs(line):

    verbs = ('edem', 'eden', 'stub', 'jebli', 'wali', 'dankt', 'tot', 'zie', 'hoi')
    words = line.split(" ")

    for word in words:
        if any(w in verbs for w in word.lower()):
            return 'True'

    return 'False'


def dutchcharpair(line):

    words = line.split(" ")

    pairs = ('ij', 'iz', 'jk', 'tst', 'lk', 'khe', 'cht')

    for word in words:
        if any(w in pairs for w in word.lower()):
            return 'True'

    return 'False'


def commonengsufx(line):

    words = line.split(" ")

    sufx = ('able', 'ness', 'ment', 'ary', 'ful', 'ive', 'less', 'ing', 'ise', 'ward', 'ing')

    for word in words:
        if word.lower().endswith(sufx):
            return 'True'


def dutchconjct(line):

    words = line.split(" ")

    conj = ('als', 'alsof', 'dat', 'sinds', 'omdat', 'town', 'tenzij', 'terwijl', 'tot', 'zoals', 'zodat', 'zolang',
            'zover', 'voor', 'hoewel', 'niet', 'het', 'ik', 'doordat', 'wie', 'zowel', 'marr', 'en', 'dus', 'onder',
            'de')

    for word in words:

        if word in conj:
            return 'True'

    return 'False'


def startsiwthchars(line):

    words = line.split(" ")

    startchar = ('z', 'w', 'v', 'kl', 'ik')

    for word in words:
        if word.lower().startswith(startchar):
            return 'True'

    return 'False'


def engwrd(line):

    shrtwrd = ('a', 'and', 'the', 'are', 'so', 'since', 'an', 'can', 'could', 'will', 'would', 'shall', 'should',
               'has', 'have', 'had', 'can\'t', 'won\'t', 'him', 'his', 'he', 'she', 'they', 'them', 'for', 'yet', 'so',
               'but', 'nor', 'together', 'only', 'unless', 'whom', 'which', 'why', 'how', 'if', 'when', 'till', 'until',
               'as', 'then', 'where', 'though')


    words = line.split(" ")

    for word in words:

        if word.lower() in shrtwrd:
            return 'True'

    return 'False'


def len5(line):

    words = line.split(" ")

    cnt = 0
    for word in words:
        if len(word) > 6:
            cnt += 1

    if cnt > 2:
        return 'True'
    else:
        return 'False'


def repeatchar(line):

    words = line.split(" ")

    repeat = ('tt', 'oo', 'aa', 'mm', 'll', 'kk')

    for word in words:
        if any(w in repeat for w in word.lower()):
            return 'True'

    return 'False'


def prefsufx(line):

    words = line.split(" ")

    k = 'False'
    suffix = ('ische', 'thie', 'thische', 'thisch', 'achtige', 'achtig', 'aar', 'ator', 'ares', 'oot', 'oaat',
              'istiek', 'isch', 'schap', 'drecht', 'etje', 'euse', 'lijk', 'lijks', 'lieden', 'foob', 'foon', 'vol'
              , 'vrij', 'vrouw', 'aat', 'aats', 'eur', 'eus', 'loog', 'geen', 'zamm', 'zuur', 'zelf', 'uur', 'trice'
              , 'sch', 'sfeer', 'nomie', 'ica', 'aan')

    preffix = ('er', 'ont', 'ver', 'eth', 'exa', 'carcino', 'cyano', 'chloor', 'buiten', 'bij', 'aan', 'aarts', 'atto'
               , 'hoodf', 'hept' , 'jood', 'tyfus', 'voor', 'weer', 'wan', 'weder', 'oor', 'onder', 'foto', 'filo')

    for word in words:
        if word.lower().startswith(preffix):
            return 'True'
        if word.lower().endswith(suffix):
            return 'True'

    return k


def test(fl, pic):
    examples = []

    f = open(fl, "r", encoding='utf-8')
    examples = []
    for line in f:
        #print(line)
        temp = []
        words = line.split("|")[1]
        temp.append(prefsufx(words))
        temp.append(repeatchar(words))
        temp.append(len5(words))
        temp.append(engwrd(words))
        temp.append(startsiwthchars(words))
        temp.append(dutchconjct(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(line.split("|")[0])

        examples.append(temp)

    print(examples)

    count = 0
    #cl = ''
    for e in examples:
        cl = dt.predict(pic, e)
        if cl == e[len(e)-1]:
            count += 1
        print("Predict for ", e[len(e)-1], " - ", )
    #print("Accuracy - ", (count / len(examples)))


def adatest(fl, pic):
    examples = []
    classes = ['nl', 'nl', 'nl', 'en', 'nl', 'nl', 'en', 'en', 'en', 'en']

    f = open(fl, "r", encoding='utf-8')
    examples = []
    for line in f:
        #print(line)
        temp = []
        words = line.split("|")[1]
        temp.append(prefsufx(words))
        temp.append(repeatchar(words))
        temp.append(len5(words))
        temp.append(engwrd(words))
        temp.append(startsiwthchars(words))
        temp.append(dutchconjct(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(prefsufx(words))
        temp.append(line.split("|")[0])

        examples.append(temp)

    print(examples)
    correct = 0
    for e in examples:
        cl = ada.predictadaboost(pic, e, classes)
        if cl > 0:
            cl = 'en'
        else:
            cl = 'nl'

        if cl == e[len(e)-1]:
            correct += 1
        print("Predict ada for ", e[len(e)-1], " - ", cl)

    print("Accuracy - ", (correct/len(examples)))


if __name__ == "__main__":

    print("Which algorithm to use for test:")
    print("1. Decision Tree (enter dt).")
    print("2. Adaboost (enter ada).")
    algo = input("Enter your choice :")

    fl = input("Enter file to use for test model : ")

    pic = input("Enter file to load model : ")

    pic = pickle.load(open(pic, 'rb'))

    if algo == 'dt':
        test(fl, pic)
    else:
        adatest(fl, pic)
