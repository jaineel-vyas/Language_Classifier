"""
    Author:    Jaineel Vyas
    Filename:   AdaBoost.py
"""


import math


class Node:
    """A decision tree node."""

    def __init__(self, examples, maxcols):

        self.left = None
        self.right = None
        self.cols = None
        self.maxcols = maxcols
        self.parentcols = []
        self.examples = examples
        self.prediction = None
        self.hypothesis = None


def calculategini11(var):
        vargini = (var[2] / (var[2] + var[5]))
        if var[0] == 0 or var[1] == 0:
            totalvarentropy = 0
        else:
            totalvarentropy = vargini * (
                        1 - (math.pow((var[0] / (var[2])), 2) + math.pow(((var[1] / (var[2]))), 2)))

        vargini = (var[5] / (var[2] + var[5]))
        if var[3] == 0 or var[4] == 0:
            totalvarentropy += 0
        else:
            totalvarentropy = vargini * (
                        1 - (math.pow((var[3] / (var[5])), 2) + math.pow(((var[4] / (var[2]))), 2)))

        return totalvarentropy

def calculategini(var):
    varentropy = (var[2] / (var[2] + var[5]))
    if var[0] == 0:
        totalvarentropy = 0
    else:
        totalvarentropy = varentropy * ((-1) * ((var[0] / (var[2])) * math.log((var[0] / (var[2])), 2)))

    if var[1] == 0:
        totalvarentropy += 0
    else:
        totalvarentropy = varentropy * ((-1) * ((var[1] / (var[2])) * math.log((var[1] / (var[2])), 2))) + totalvarentropy

    varentropy = (var[5] / (var[2] + var[5]))
    if var[3] == 0:
        totalvarentropy += 0
    else:
        totalvarentropy = varentropy * ((-1) * ((var[3] / (var[5])) * math.log((var[3] / (var[5])), 2))) + totalvarentropy

    if var[4] == 0:
        totalvarentropy += 0
    else:
        totalvarentropy = varentropy * ((-1) * ((var[4] / (var[5])) * math.log((var[4] / (var[5])), 2))) + totalvarentropy
    return totalvarentropy


def learn_grow_tree(node):

        already_selected = node.parentcols

        varcnts = []

        print("\nParent - ", node.parentcols)
        print("Examples to be filtered furthur - ", len(node.examples))
        if len(node.parentcols) > 0:
            if len(node.parentcols) > 8:
                return

        temp = [
            [0, 0, 0,0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        acnt = 0
        bcnt = 0
        print(node.maxcols)
        colcnt = 0
        found = 0
        found1 = 0
        for line in node.examples:
                for i in range(node.maxcols-1):
                    #if len(already_selected) > 0:
                    if i in already_selected:
                        i += 1
                        continue
                    else:
                        if line[i] == 'True' and line[len(line)-2] == 'en':
                            temp[i][0] += line[len(line)-1]
                            temp[i][2] += line[len(line)-1]
                            found += 1
                        elif line[i] == 'True' and line[len(line)-2] == 'nl':
                            temp[i][1] += line[len(line)-1]
                            temp[i][2] += line[len(line)-1]
                            found += 1
                        elif line[i] == 'False' and line[len(line)-2] == 'en':
                            temp[i][3] += line[len(line)-1]
                            temp[i][5] += line[len(line)-1]
                            found1 += 1
                        elif line[i] == 'False' and line[len(line)-2] == 'nl':
                            temp[i][4] += line[len(line)-1]
                            temp[i][5] += line[len(line)-1]
                            found1 += 1
                        i += 1
                    #varcnts.append(temp)
                    #print(temp)
                if line[len(line)-1] == 'en':
                    acnt += 1
                else:
                    bcnt += 1
                #break;

        if acnt > bcnt:
            node.prediction = 'en'
        else:
            node.prediction = 'nl'
        print(temp)
        ginis = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100]

        giniroot = 1 - (math.pow((acnt / (acnt + bcnt)), 2) + math.pow((bcnt / (acnt + bcnt)), 2))

        if found == 0 or found1 == 0:
            return node

        for i in range(node.maxcols-2):
            #if len(already_selected) > 0:
            if i in already_selected:
                    continue
            else:
                ginis[i] = giniroot - calculategini(temp[i])
            print("i = ", i)

        print(ginis)

        mx = -100
        for g in ginis:
            if g > mx and g != 0:
                mx = g

        if mx == -100:
            return node
        select = ginis.index(mx)

        print("Selected - " , select)
        node.cols = select

        if select == 0:
            left = 'nl'
            right = 'en'
        elif select == 1:
            left = 'nl'
            right = 'en'
        elif select == 2:
            left = 'nl'
            right = 'en'
        elif select == 3:
            left = 'en'
            right = 'nl'
        elif select == 4:
            left = 'nl'
            right = 'en'
        elif select == 5:
            left = 'nl'
            right = 'en'
        elif select == 6:
            left = 'nl'
            right = 'en'
        elif select == 7:
            left = 'en'
            right = 'nl'
        elif select == 8:
            left = 'nl'
            right = 'en'
        elif select == 9:
            left = 'en'
            right = 'nl'

        node.left = left
        node.right = right

        return node


def predict(root, test):


    for i in range(len(test)):
        col = root.cols
        if col == None:
            return root.prediction
        print("parents - " , root.parentcols , " and selected is ", root.cols)
        classify = root.prediction
        if test[col] == 'True':
            if root.left != None:
                root = root.left
            else:
                return classify
        else:
            if root.right != None:
                root = root.right
            else:
                return classify
        i += 1
    return classify


def adaboost(node, v, classes):

    classifiers = []

    cnt = 0
    while cnt < v:
        node = learn_grow_tree(node)

        if cnt == 0:
            for e in node.examples:
                e[len(e) - 1] = 1 / (len(node.examples))

        intrue = classes[node.cols]

        maxlen = len(node.examples[0])
        maxweight = 0

        totalincorrectweight = 0
        for e in node.examples:
            if e[node.cols] == 'True' and e[maxlen - 2] != intrue:
                totalincorrectweight += e[maxlen - 1]
            if e[node.cols] == 'False' and e[maxlen - 2] == intrue:
                totalincorrectweight += e[maxlen - 1]
        hyposweight = (math.log((1 - totalincorrectweight) / totalincorrectweight, 10))

        for e in node.examples:
            if e[node.cols] == 'True' and e[maxlen - 2] != intrue:
                e[maxlen - 1] = e[maxlen-1] * math.exp(hyposweight)
            if e[node.cols] == 'False' and e[maxlen - 2] == intrue:
                e[maxlen - 1] = e[maxlen - 1] * math.exp(hyposweight)
            else:
                e[maxlen - 1] = e[maxlen - 1] * math.exp(-1 * hyposweight)
            maxweight += e[maxlen-1]

        for e in node.examples:
            e[maxlen - 1] = e[maxlen - 1] / maxweight

        node.hypothesis = hyposweight

        classifiers.append(node)

        node = Node(node.examples, len(node.examples[0]))

        cnt += 1

    return classifiers

def predictadaboost(node, test, classes):

    totalweight = 0

    for e in node:
        if test[e.cols] == 'True':
            if e.left == 'en':
                totalweight += abs(e.hypothesis)
            # elif e.left == 'nl':
            #     totalweight -= abs(e.hypothesis)
        elif test[e.cols] == 'False':
            # if e.left == 'en':
            #     totalweight += abs(e.hypothesis)
            if e.left == 'nl':
                totalweight -= abs(e.hypothesis)
        #print("totalweight for ", e.cols , "now - ", totalweight)

    return totalweight

# Use this to test only the AdaBoost algorithm for classifying
if __name__ == "__main__":

    f = open("train10000", "r", encoding='utf-8')
    examples = []
    classes = ['nl', 'nl', 'nl', 'en', 'nl', 'nl', 'nl', 'en', 'en', 'en']

    for line in f:
        entries = line.split(" ")
        colcnt = 0
        temp = []
        for e in entries:
            temp.append(e.replace(" ", "").replace("\n", ""))

        temp.append(1)
        examples.append(temp)

    print(examples[0], " - length = ", len(examples[0]))
    node = Node(examples, len(examples[0]))
    tree = adaboost(node, 10, classes)

    print("Class - ", predictadaboost(tree, ['True', 'True', 'False', 'False', 'True', 'False', 'False', 'True']), classes)
