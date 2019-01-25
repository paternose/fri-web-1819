from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm
from math import log



def extractRawLines():
    path1 = "/home/insight/Documents/OSY/RechercheWeb/FRI_WEB_2018_2019/Cours/Projet/Data/CACM/"
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



"""Vectorial Search"""
def tf(term,document):
    tokenizer = RegexpTokenizer(r'\w+')
    return sum([tokenizer.tokenize(document[i].lower()).count(term.lower()) for i in range(len(document))])

def tf_index(term, document_id, index):
    if term in index.keys():
        if document_id in index[term].keys():
            return index[term][document_id]
        else:
            return 0
    else:
        return 0

def idf(term, index, length):
    """"we give length=len(collection) as an argument to avoid calculating it at each iteration"""
    try:
        return log(length/len(index[term.lower()]))
    except KeyError:
        return 0

def pTf(term, document):
    return tf(term, document)

def pTf_index(term, document, index):
    return tf_index(term, document, index)

def pDf(term, index, length):
    return 1

def vectorialSearch(query, collection, index):
    length=len(collection)
    query_words=query.split()
    Nd=dict()

    for doc in collection.keys():
        Nd[doc]=sum([1 for document in collection])
    Nq=0
    score=dict()
    for j in collection.keys():
        score[j]=0
    W=dict()
    W['query_words']=dict()
    for query_word in query_words:
        try:
            # print("query_words",query_words)
            # print("collection",collection)
            W['query_words'][query_word]=pTf(query_word,query)*pDf(query_word, index, length)
            Nq+=(W['query_words'][query_word])**2
            L=index[query_word].keys()
            # print("L", L)

            for j in L:
                try:
                    W[j][query_words[i - 1]]=Nd[j]*pTf_index(query_word,j, index)*pDf(query_word, index, length)
                #if j not in W keys
                except:
                    W[j]=dict()
                    W[j][query_word]=Nd[j]*pTf_index(query_word,j, index)*pDf(query_word, index, length)
                score[j]+=(W[j][query_word])**2
        except KeyError:
            pass
    for j in collection.keys():
        if ((Nd[j]*Nq)**0.5)!=0:
            score[j]=score[j]/((Nd[j]*Nq)**0.5)

    return score

if __name__ == '__main__':
    raw_lines = extractRawLines()
    research_expr = "AND(NOT('formally'), OR('lecture', 'straightforward', 'formally'))"
    print("Extracting docs:")
    docs = extractDocs(raw_lines)
    print("{} documents found.".format(len(docs.keys())))
    #    print(docs)
    print("Extracting index ...")
    index = invertBlock(docs)
    print("index size : ", len(index.keys()))
    #    print(index.keys())
    print("Executing research ...")
    research_result = research(index, set(docs.keys()), research_expr)
    print("Results from research {} :".format(research_expr))
    print(research_result)
    print(index['lecture'])
    #    print(index['straightforward'])
    print(index['formally'])

    print("\nVectorial Search Test\n")
    print("Query : ", "'projects'")
    scores=vectorialSearch("projects", docs, index)
    print("scores",scores)
    print("Score of document 1 that do not contain 'projects' :", scores[1])
    print("Score of document 1735 that contains 'projects' :", scores[1735])
    print("Score of document 2311 that contains 'projects' :", scores[2311])

    print("\nInverted index test\n")
    block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc aaa\n", "ddd\n"], 3: ["ccc\n", "eee\n"]}
    print("Block example", block)
    print("Inverted index", invertBlock(block))
