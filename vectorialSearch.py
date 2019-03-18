from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm
from math import log
from bsbi import*
import time
import operator


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

def generate_nd(collection, normalized = False):
    tokenizer = RegexpTokenizer(r'\w+')
    nd = dict()
    for doc in collection.keys():
        nd[doc]=1.
    if not normalized:
        return nd

    for doc in collection.keys():
        nbr_words = 0.
        for line in collection[doc]:
            nbr_words += len(tokenizer.tokenize(line))
        nd[doc] /= nbr_words**.5

    return nd

def vectorialSearch(query, collection, index, pTf, pTf_index, pDf, generate_nd):
    length=len(collection)
    query_words=query.split()
    Nd=generate_nd(collection)

    # for doc in collection.keys():
    #     Nd[doc]=1
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
    docs = extractDocs(raw_lines)
    t1=time.time()
    index = invertBlock(docs)
    t2=time.time()
    print("\n\nIndexaton time :", t2-t1,)

    print("\nVectorial Search Test and Evaluation\n")
    print('Test 1 : ptf=tf, pdf=1, Nd=1\n')

    for query in ['solve differential equations',
                  'What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?'
                     ]:
        print("\n\nQuery : '", query,"'")
        t1 = time.time()
        scores = vectorialSearch(query, docs, index, pTf, pTf_index, pDf, generate_nd)
        sorted_scores = sorted(scores.items(), key=lambda kv: kv[1])
        t2 = time.time()
        print("Response time for this query :", t2 - t1)
        print("\nThose are the best results : ")
        for i in range(1, 10):
            print("\tDocument", sorted_scores[-i][0], "with a score :", sorted_scores[-i][1])


    print("")
    print("Query (single word) : ", "'projects'")
    scores = vectorialSearch("projects", docs, index, pTf, pTf_index, pDf, generate_nd)
    print("\tScore of document 1 that do not contain 'projects' :", scores[1])
    print("\tScore of document 1735 that contains 'projects' :", scores[1735])
    print("\tScore of document 2311 that contains 'projects' :", scores[2311])



