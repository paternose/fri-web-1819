from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm


def extractRawLines():
    path1="/home/insight/Documents/OSY/RechercheWeb/FRI_WEB_2018_2019/Cours/Projet/Data/CACM/"
    path2="/mnt/f/etudes/OSY/recherche_web/Data/Data/CACM/"
    raw_lines = []
    print("Loading file ..")
    try:
        f=open(path1 + "cacm.all","r")
        raw_lines=f.readlines()
        f.close()
    except:
        None
    try:
        f=open(path2 + "cacm.all","r")
        raw_lines=f.readlines()
        f.close()
    except:
        None
    return raw_lines
    

def extractDocs(raw_lines):
    docs = {}
    current_doc = ''
    i = 0
    reading = False

    for line in tqdm(raw_lines):
        if line[0]==".":
            if line[0:2] == ".I":
                if len(current_doc):
                    docs[i] = current_doc[:]
                    i += 1
                current_doc = ''
            elif line[0:2] in [".K",".T",".W"]:
                reading = True
            else:
                reading = False
        else:
            if reading:
                current_doc += line

    return docs

def getBlock(docs, docIds, length_limit):
    counter=0
    block=dict()
    i=0
    for doc in docs:
        if counter+len(doc)<=length_limit: block[docIds[i]]=doc
        i+=1
    return block

def extractTokens(lines):
    ## Takes an array of lines as input, returns an array of tokens (with
    # duplicates)
    tokens = []
    tokenizer = RegexpTokenizer(r'\w+')
    for line in lines:
        for token in tokenizer.tokenize(line):
            if token not in tokens:
                tokens.append(token)
    return tokens



"""
block example: key: documentId, value: lines
block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc cc\n", "ddd\n"],3: ["ccc\n","eee\n"]}
"""
def countToken(token, lines):
    counter=0
    tokenizer = RegexpTokenizer(r'\w+')
    for line in lines:
        counter+=tokenizer.tokenize(line).count(token)
    return counter

def invertBlock(block):
    invertedIndex = dict()
    for documentId in tqdm(block.keys()):
        for token in extractTokens(block[documentId]):
            try:
                invertedIndex[token].add((documentId,countToken(token, block[documentId])))
            except:
                invertedIndex[token]={(documentId, countToken(token,block[documentId]))}
    return invertedIndex


def createIndex():
    index = dict()
    raw_lines = extractRawLines()
    docs_lines = extractDocs(raw_lines)
    index = dict()
#    index = invertBlock(docs_lines)
    return index



if __name__ == '__main__':
    raw_lines = extractRawLines()
    
    print("Extracting docs:")
    docs = extractDocs(raw_lines)
    print("{} documents found.".format(len(docs.keys())))
    print("Extracting index ...")
    index = invertBlock(docs)
    print("index size : ", len(index.keys()))
    print(index.keys())
    block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc aaa\n", "ddd\n"], 3: ["ccc\n", "eee\n"]}
    print("Exemple de block", block)
    print("Index inversé", invertBlock(block))
