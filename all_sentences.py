import os
from nltk.tokenize import RegexpTokenizer


def extractLines(lines):
    sentences=[]
    reading = False
    for line in lines:
        if line[0]==".":
            if line[0:2] in [".K",".T",".W"]:
                reading = True
            else:
                reading = False
        else:
            if reading:
                sentences.append(line)
    return sentences

def extractTokens(lines):
    tokens=dict()
    tokenizer = RegexpTokenizer(r'\w+')
    nbrTokens = 0
    for sentence in lines:
        for token in tokenizer.tokenize(sentence):
            nbrTokens += 1
            try:
                tokens[token.lower()]+=1

            #si le token n'est pas encore dans le dictionnaire
            except:
                tokens[token.lower()]=1

    print("Number of tokens : {}".format(nbrTokens))
    print("Vocabulary size : {}".format(len(tokens)))
    return tokens
    #print(tokens)


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
    
    processed_lines = extractLines(raw_lines)
    tokens = extractTokens(processed_lines[:int(len(processed_lines)/2)])
    tokens = extractTokens(processed_lines)

    
