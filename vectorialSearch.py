from math import log
from nltk.tokenize import RegexpTokenizer



def tf(term,document):
    tokenizer = RegexpTokenizer(r'\w+')
    #potential optimization: remove count and make loop instead
    return sum([tokenizer.tokenize(document[i].lower()).count(term.lower()) for i in range(len(document))])
def idf(term, collection):
    return log(length/len(index[term.lower()]))

def vectorialSearch(query, collection, index):
    query_tokens=query.split()
    Nd=dict()
    for doc in collection.keys():
        Nd[doc]=sum([1 for document in collection])
    Nq=0 
    score=dict()
    for j in range(1,length+1):
        score[j]=0
    W=dict()
    W['query_tokens']=dict()
    for i in range(1,len(query_tokens)+1):
        # print("query_tokens",query_tokens)
        # print("collection",collection)
        W['query_tokens'][query_tokens[i-1]]=tf(query_tokens[i-1],query)*idf(query_tokens[i-1], collection)
        Nq+=(W['query_tokens'][query_tokens[i-1]])**2
        L=index[query_tokens[i-1]].keys()
        # print("L", L)

        for j in L:
            try:
                W[j][query_tokens[i - 1]]=Nd[j]*tf(query_tokens[i-1],C[j])*idf(query_tokens[i-1], collection)
            #if j not in W keys
            except:
                W[j]=dict()
                W[j][query_tokens[i - 1]]=Nd[j]*tf(query_tokens[i-1],C[j])*idf(query_tokens[i-1], collection)
            score[j]+=(W[j][query_tokens[i-1]])**2

    for j in range(1,len(collection)+1):
        if ((Nd[j]*Nq)**0.5)!=0:
            score[j]=score[j]/((Nd[j]*Nq)**0.5)

    return score

if __name__ == '__main__':
    C = {1: ["aaa aaa eee\n", "bbb\n"], 2: ["ccc \n", "ddd\n"], 3: ["ccc eee\n", "a\n"]}
    length=len(C)
    #index: the output of bsbi.py
    index={'bbb': {1: 1}, 'eee': {1:2, 3: 1}, 'aaa': {1: 2, 2: 1}, 'ddd': {2: 1}, 'ccc': {2: 1, 3: 1}}
    print("Le document 2 est le seul qui ne contient pas 'eee' ")
    print(vectorialSearch("eee", C, index))
    print("")
    print("Le document 2 est le seul qui ne contient pas 'eee' mais il contient 'ccc' ")
    print(vectorialSearch("eee ccc", C, index))










