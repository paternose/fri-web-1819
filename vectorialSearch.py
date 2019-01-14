from math import log
from nltk.tokenize import RegexpTokenizer



def tf(term,document):
    tokenizer = RegexpTokenizer(r'\w+')
    #potential optimization: remove count and make loop instead
    return sum([tokenizer.tokenize(document[i].lower()).count(term.lower()) for i in range(len(document))])
def idf(term, collection, length):
    """"we give length=len(collection) as an argument to avoid calculating it at each iteration"""
    return log(length/len(index[term.lower()]))

def vectorialSearch(query, collection, index):
    length=len(collection)
    query_words=query.split()
    Nd=dict()

    for doc in collection.keys():
        Nd[doc]=sum([1 for document in collection])
    Nq=0
    score=dict()
    for j in range(1,length+1):
        score[j]=0
    W=dict()
    W['query_words']=dict()
    for i in range(1,len(query_words)+1):
        # print("query_words",query_words)
        # print("collection",collection)
        W['query_words'][query_words[i-1]]=tf(query_words[i-1],query)*idf(query_words[i-1], collection, length)
        Nq+=(W['query_words'][query_words[i-1]])**2
        L=index[query_words[i-1]].keys()
        # print("L", L)

        for j in L:
            try:
                W[j][query_words[i - 1]]=Nd[j]*tf(query_words[i-1],C[j])*idf(query_words[i-1], collection, length)
            #if j not in W keys
            except:
                W[j]=dict()
                W[j][query_words[i - 1]]=Nd[j]*tf(query_words[i-1],C[j])*idf(query_words[i-1], collection, length)
            score[j]+=(W[j][query_words[i-1]])**2

    for j in range(1,len(collection)+1):
        if ((Nd[j]*Nq)**0.5)!=0:
            score[j]=score[j]/((Nd[j]*Nq)**0.5)

    return score

if __name__ == '__main__':
    C = {1: ["aaa aaa eee\n", "bbb\n"], 2: ["ccc \n", "ddd\n"], 3: ["ccc eee\n", "a\n"]}
    # length=len(C)
    #index: the output of bsbi.py
    index={'bbb': {1: 1}, 'eee': {1:2, 3: 1}, 'aaa': {1: 2, 2: 1}, 'ddd': {2: 1}, 'ccc': {2: 1, 3: 1}}
    print("Query : ", "'bbb'")
    print("Document 1 is the only one containing 'bbb' ")
    print(vectorialSearch("bbb", C, index),"\n")

    print("Query : ", "'eee'")
    print("Document 2 is the only one not containing  'eee' ")
    print(vectorialSearch("eee", C, index),"\n")

    print("Query : ", "'eee ccc'")
    print("Document 2 is the only one not containing 'eee'  but containing 'ccc' ")
    print("Document 1 and 2 have the same score. Document 3 has higher score because he contains both of the tokens 'eee' and 'ccc' ")
    print(vectorialSearch("eee ccc", C, index))










