import os
from nltk.tokenize import RegexpTokenizer


l = []
try:
    path="/home/insight/Documents/OSY/RechercheWeb/FRI_WEB_2018_2019/Cours/Projet/Data/CACM/"
    os.chdir(path)
    f=open("cacm.all","r")
    l=f.readlines()
    f.close()
except:
    None
try:
    path="/mnt/f/etudes/OSY/recherche_web/Data/Data/CACM/"
    os.chdir(path)
    f=open("cacm.all","r")
    l=f.readlines()
    f.close()
except:
    None
sentences=[]

reading = False
for line in l:
    if line[0]==".":
        if line[0:2] in [".K",".T",".W"]:
            reading = True
        else:
            reading = False
    else:
        if reading:
            sentences.append(line)

tokens=dict()
tokenizer = RegexpTokenizer(r'\w+')
for sentence in sentences:
    for token in tokenizer.tokenize(sentence):
        try:
            tokens[token.lower()]+=1

        #si le token n'est pas encore dans le dictionnaire
        except:
            tokens[token.lower()]=1

