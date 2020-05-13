"""
    Author:    Jaineel Vyas
    Filename:   DecisionT.py
"""

import math


class Node:
    """A decision tree node."""

    def __init__(self, examples, maxcols):
        '''
            Initialize a node with examples(data array rows).
        :param examples: data array
        :param maxcols: number of columns in the data array
        '''
        self.left = None
        self.right = None
        self.cols = None            # stores the selected column number (attribute selected at current node)
        self.maxcols = maxcols
        self.parentcols = []        # list of parent columns of the current node
        self.examples = examples
        self.prediction = None      # the class to be given out as prediction corresponding to the current node


def calculateginitest(var):
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
    '''
    Takes an array containing incorrect and correct count of attributes
    :param var: array containing counts of an attribute
    :return: ginivalue of an attribute
    '''
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
    '''
        Takes node and selects best attribute for that node.
        Recursively creates left and ride child node, assuming left child to be associated with
        True value of current node and right child with False value of current attribute.
    :param node: starts with root node, each node represent an attribute
    :return: node returned with selected best attribute and predicted class
    '''
    already_selected = node.parentcols

    if len(node.parentcols) > 0:
        if len(node.parentcols) > 8:
            return

    temp = [[0 for i in range(6)] for r in range(node.maxcols)]

    acnt = 0
    bcnt = 0
    #print(node.maxcols)
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
                if line[i] == 'True' and line[len(line)-1] == 'en':
                    temp[i][0] += 1
                    temp[i][2] += 1
                    found += 1
                elif line[i] == 'True' and line[len(line)-1] == 'nl':
                    temp[i][1] += 1
                    temp[i][2] += 1
                    found += 1
                elif line[i] == 'False' and line[len(line)-1] == 'en':
                    temp[i][3] += 1
                    temp[i][5] += 1
                    found1 += 1
                elif line[i] == 'False' and line[len(line)-1] == 'nl':
                    temp[i][4] += 1
                    temp[i][5] += 1
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

    #print(acnt)
    #print(temp)
    ginis = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100]

    giniroot = 1 - (math.pow((acnt / (acnt + bcnt)), 2) + math.pow((bcnt / (acnt + bcnt)), 2))

    if found == 0 or found1 == 0:
        return node

    for i in range(node.maxcols-1):
        if i in already_selected:
            continue
        else:
            ginis[i] = giniroot - calculategini(temp[i])

    #print(ginis)
    mx = -100
    for g in ginis:
        if g > mx and g != 0:
            mx = g

    if mx == -100:
        return node
    select = ginis.index(mx)

    #print("Selected - " , select)
    node.cols = select

    left = []
    right = []
    for line1 in node.examples:
        if line1[select] == 'True':
            left.append(line1)
        else:
            right.append(line1)

    if len(left) > 0:
        #print("max cols left - ", len(left[0]), " of ", left[0])
        nodechild = Node(left, len(left[0]))
        for n in node.parentcols:
            nodechild.parentcols.append(n)
        nodechild.parentcols.append(select)

        node.left = learn_grow_tree(nodechild)

    if len(right) > 0:
        #print("max cols right - ", len(right[0]), " of ", right[0])
        nodechildr = Node(right, len(right[0]))
        for n in node.parentcols:
            nodechildr.parentcols.append(n)
        nodechildr.parentcols.append(select)

        node.right = learn_grow_tree(nodechildr)
    return node


def predict(root, test):
    '''
        Function to run the prediction.
    :param root: the root node of decision tree
    :param test: the test data (1 row at a time as input)
    :return: the class selected for the test data
    '''

    for i in range(len(test)):
        col = root.cols
        if col == None:
            return root.prediction
        #print("parents - " , root.parentcols , " and selected is ", root.cols)
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

# Use only to test the decisiontree algorithm for classifying
if __name__ == "__main__":

    f = open("new5000.txt", "r")
    examples = []

    for line in f:
        entries = line.split(" ")
        colcnt = 0
        temp = []
        for e in entries:
            temp.append(e.replace(" ", "").replace("\n", ""))
        examples.append(temp)

    print(examples[0], " - length = ", len(examples[0]))
    node = Node(examples, len(examples[0]))
    tree = learn_grow_tree(node)
    print("Predict - ", predict(node, ['True', 'True', 'False', 'False', 'True', 'False', 'False', 'True']))