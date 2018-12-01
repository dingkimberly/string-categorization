from process import make_vectors, process, make_test_vectors
import numpy as np
from sklearn import random_projection
from sklearn.metrics.pairwise import cosine_similarity
import functools
import time


def hyperplanes(X):
    transformer = random_projection.GaussianRandomProjection()
    print(X.shape)
    X_new = transformer.fit_transform(X)
    print(X_new.shape)

    return X_new


def cosine_similarity_wrap(vec_to_compare):
    return functools.partial(cosine_similarity, vec_to_compare)
   

def t():
    global start
    try:
        end = time.time()
        print("time elapsed: ", end - start)
        start = time.time()
    except NameError:
        start = time.time()
    return 


def test(X, Y, Xtest, Ytest):
    print(Y.shape)
    print(Ytest.shape)
    errors = 0

    for i1, current_row in enumerate(Xtest):
        cos_sim = cosine_similarity_wrap(current_row)
        
        max_sim = 0
        max_sim_indexes = []

        for i2, row in enumerate(X):
            sim = cos_sim(row)
            if sim[0,0] > max_sim:
                max_sim = sim[0,0]
                max_sim_indexes = [i2]
            elif sim[0,0] == max_sim:
                max_sim_indexes.append(i2)
        
        t()
        print((i1*X.shape[0]+i2)/(X.shape[0]*Xtest.shape[0])*100, "%")
        cats = set(list(map(lambda x: Y[x,0], max_sim_indexes)))
        if Ytest[i1,0] not in cats:
            errors += 1
            print("errors: ", errors/(i1+1)*100, "%")
    return 




if __name__ == "__main__":
    xtrain, xtest, ytrain, ytest = process()
    X, Y, index_to_word, word_to_index = make_vectors(xtrain, ytrain)
    Xtest, Ytest = make_test_vectors(xtest,ytest, word_to_index) 
    test(X, Y, Xtest, Ytest)
