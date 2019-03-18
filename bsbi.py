from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm
from math import log
import time


def extractRawLines():
    path1 = "/home/insight/Documents/OSY/RechercheWeb/cacm/"
    path2 = "/mnt/f/etudes/OSY/recherche_web/Data/Data/CACM/"
    raw_lines = []
    print("Loading file ..")
    try:
        f = open(path1 + "cacm.all", "r")
        raw_lines = f.readlines()
        f.close()
    except:
        None
    try:
        f = open(path2 + "cacm.all", "r")
        raw_lines = f.readlines()
        f.close()
    except:
        None
    return raw_lines


def extractDocs(raw_lines):
    docs = {}
    current_doc = []
    i = 1
    reading = False

    for line in tqdm(raw_lines):
        if line[0] == ".":
            if line[0:2] == ".I":
                if len(current_doc):
                    docs[i] = current_doc[:]
                    i += 1
                current_doc = []
            elif line[0:2] in [".K", ".T", ".W"]:
                reading = True
            else:
                reading = False
        else:
            if reading:
                current_doc.append(line)

    return docs


def getBlock(docs, docIds, length_limit):
    counter = 0
    block = dict()
    i = 0
    for doc in docs:
        if counter + len(doc) <= length_limit: block[docIds[i]] = doc
        i += 1
    return block


def extractTokens(lines):
    ## Takes an array of lines as input, returns an array of tokens (with
    # duplicates)
    tokens = []
    tokenizer = RegexpTokenizer(r'\w+')
    for line in lines:
        for token in tokenizer.tokenize(line.lower()):
            if token not in tokens:
                tokens.append(token)
    return tokens


"""
block example: key: documentId, value: lines
block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc cc\n", "ddd\n"],3: ["ccc\n","eee\n"]}
"""


def countToken(token, lines):
    counter = 0
    tokenizer = RegexpTokenizer(r'\w+')
    for line in lines:
        counter += tokenizer.tokenize(line).count(token.lower())
    return counter


def invertBlock(block):
    invertedIndex = dict()
    tokenizer = RegexpTokenizer(r'\w+')
    for documentId in tqdm(block.keys()):
        for line in block[documentId]:
            for token in tokenizer.tokenize(line.lower()):

                try:
                    invertedIndex[token][documentId] += 1
                except:
                    try:
                        invertedIndex[token][documentId] = 1
                    except:
                        invertedIndex[token] = dict()
                        invertedIndex[token][documentId] = 1

    return invertedIndex


def createIndex():
    index = dict()
    raw_lines = extractRawLines()
    docs_lines = extractDocs(raw_lines)
    index = dict()
    #    index = invertBlock(docs_lines)
    return index


def findDocsWith(index, token):
    docs = []
    if type(token) is set:
        return token
    else:
        if token in index.keys():
            for doc in index[token].keys():
                docs.append(doc)
        return set(docs)


def operatorOR(set1, set2):
    return set1 | set2


def operatorAND(set1, set2):
    return set1 & set2


def operatorNOT(index, doc_set, token):
    return doc_set - findDocsWith(index, token)


def operatorMultiOR(index, *arg):
    return operatorMulti(index, operatorOR, *arg)


def operatorMultiAND(index, *arg):
    return operatorMulti(index, operatorAND, *arg)


def operatorMulti(index, func, *arg):
    currentSet = findDocsWith(index, arg[0])
    for i in range(1, len(arg)):
        currentSet = func(currentSet, findDocsWith(index, arg[i]))
    return currentSet


def research(index, doc_set, expression):
    print("Starting expression : {}".format(expression))
    expression = expression.replace('OR(', 'operatorMultiOR(index, ')
    expression = expression.replace('AND(', 'operatorMultiAND(index, ')
    expression = expression.replace('NOT(', 'operatorNOT(index, doc_set, ')
    print("Corrected expression : {}".format(expression))
    return eval(expression)



if __name__ == '__main__':
    print("\nInverted index demo\n")
    block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc aaa\n", "ddd\n"], 3: ["ccc\n", "eee\n"]}
    print("Block example", block)
    print("Inverted index", invertBlock(block))

    raw_lines = extractRawLines()
    research_expr = "AND(NOT('formally'), OR('lecture', 'straightforward', 'formally'))"
    print("Extracting docs:")
    docs = extractDocs(raw_lines)
    print("{} documents found   .".format(len(docs.keys())))
    #    print(docs)
    print("Extracting index ...")
    t1 = time.time()
    index = invertBlock(docs)
    t2 = time.time()
    print("\n\nIndexaton time :", t2 - t1, )
    print("index size : ", len(index.keys()))
    #    print(index.keys())
    print("Executing research ...")
    research_result = research(index, set(docs.keys()), research_expr)
    print("Results from research {} :".format(research_expr))
    print(research_result)
    print(index['lecture'])
    #    print(index['straightforward'])
    print(index['formally'])


