import os
import math
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as pp


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
    return (tokens, nbrTokens)
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
    nbrT1 = 0
    nbrT2 = 0
    (tokens2, nbrT2) = extractTokens(processed_lines[:int(len(processed_lines)/2)])
    (tokens1, nbrT1) = extractTokens(processed_lines)
    nbrM1 = len(tokens1)
    nbrM2 = len(tokens2)
    var_b = (math.log(nbrM1) - math.log(nbrM2)) / math.log(nbrT1/nbrT2)
    var_k = nbrM1/math.pow(nbrT1, var_b)
    print("Result : (k:{}) (b:{})".format(var_k, var_b))
    print("Prediction for 100.000 tokens : {}".format(var_k * math.pow(100000, var_b)))
    print("Prediction for 1.000.000 tokens : {}".format(var_k * math.pow(1000000, var_b)))

    #set pour éliminer les doublons
    frequences=list(set(tokens1.values()))
    frequences.sort()
    rangs=[frequences.index(e)+1 for e in frequences]
    log_frequences=[math.log(e) for e in frequences]
    log_rangs=[math.log(e) for e in rangs]

    pp.subplot(2, 1, 1)
    pp.plot(rangs,frequences)
    pp.xlabel("rang")
    pp.ylabel("frequence")


    pp.subplot(2, 1, 2)
    pp.plot(log_rangs,log_frequences)
    pp.xlabel("log(rang)")
    pp.ylabel("log(frequence)")
    pp.show()


    

