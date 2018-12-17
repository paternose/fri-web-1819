from nltk.tokenize import RegexpTokenizer



def extractDocs(raw_lines):
    docs = []
    current_doc = []
    
    reading = False
    for line in raw_lines:
        if line[0]==".":
            if line[0:2] == ".I":
                if len(current_doc):
                    docs.append(current_doc[:])
                current_doc = []
            elif line[0:2] in [".K",".T",".W"]:
                reading = True
            else:
                reading = False
        else:
            if reading:
                current_doc.append(line)

    return docs

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
    for documentId in block.keys():
        for token in extractTokens(block[documentId]):
            try:
                invertedIndex[token].add((documentId,countToken(token, block[documentId])))
            except:
                invertedIndex[token]={(documentId, countToken(token,block[documentId]))}
    return invertedIndex


if __name__ == '__main__':
    # lancement du serveur
    path1="/home/insight/Documents/OSY/RechercheWeb/FRI_WEB_2018_2019/Cours/Projet/Data/CACM/"
    path2="/mnt/f/etudes/OSY/recherche_web/Data/Data/CACM/"
    raw_lines = []
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
    
    docs_lines = extractDocs(raw_lines)
    doc_tokens = []
    for doc in docs_lines:
        doc_tokens.append(extractTokens(doc))
    print("{} docs extracted.".format(len(doc_tokens)))
    block = {1: ["aaa aaa\n", "bbb\n"], 2: ["ccc aaa\n", "ddd\n"], 3: ["ccc\n", "eee\n"]}
    print("Exemple de block", block)
    print("Index inversé", invertBlock(block))