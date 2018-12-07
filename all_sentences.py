

import os
path="/home/insight/Documents/OSY/RechercheWeb/FRI_WEB_2018_2019/Cours/Projet/Data/CACM/"
os.chdir(path)
f=open("cacm.all","r")
l=f.readlines()
f.close()
sentences=[]
i=0
while i<len(l):

    if l[i][0:2] in [".K",".I",".W"]:
        j=i
        while j<len(l):
            if l[j][0]!=".": sentences.append(l[j])
            j+=1
        i=j
    else: i+=1


print(sentences)