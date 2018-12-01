from process import make_vectors, process, make_test_vectors
import numpy as np
from sklearn import random_projection
from sklearn.metrics.pairwise import cosine_similarity
import functools
import time
from multiprocessing import Pool, cpu_count

total = 0
errors = 0

def hyperplanes(X):
    transformer = random_projection.GaussianRandomProjection()
    print(X.shape)
    X_new = transformer.fit_transform(X)
    print(X_new.shape)

    return X_new


def cosine_similarity_wrap(vec_to_compare):
    return functools.partial(cosine_similarity, vec_to_compare)


def csp_partial(X, Y, Xtest):
    return functools.partial(cosine_similarity_pool_map, X, Y, Xtest)

def cosine_similarity_pool_map(X, Y, Xtest, params):
    cos_sim = cosine_similarity_wrap(Xtest[params[0],:])
    max_sim = 0
    max_sim_indexes = []

    for i, row in enumerate(X):
        sim = cos_sim(row)
        if sim[0,0] > max_sim:
            max_sim = sim[0,0]
            max_sim_indexes = [i]
        elif sim[0,0] == max_sim:
            max_sim_indexes.append(i)

    cats = set(list(map(lambda x: Y[x,0], max_sim_indexes)))
    if params[1] not in cats:
        print(cats, params[1])
        return False
    return True

def pooled_test(X, Y, Xtest, Ytest):
    csp = csp_partial(X,Y,Xtest)

    p = Pool(cpu_count())
    correct_list = p.map(csp, list(zip(list(range(Xtest.shape[0])), \
            map(lambda x: x[0],Ytest.tolist()))))
    print(correct_list)


def t():
    global start
    try:
        end = time.time()
        print("time elapsed: ", end - start)
        start = time.time()
    except NameError:
        start = time.time()
    return 




# def test(X, Y, Xtest, Ytest):
#     errors = 0

#     for i1, current_row in enumerate(Xtest):
#         cos_sim = cosine_similarity_wrap(current_row)
        
#         max_sim = 0
#         max_sim_indexes = []

#         for i2, row in enumerate(X):
#             sim = cos_sim(row)
#             if sim[0,0] > max_sim:
#                 max_sim = sim[0,0]
#                 max_sim_indexes = [i2]
#             elif sim[0,0] == max_sim:
#                 max_sim_indexes.append(i2)
        
#         t()
#         print((i1*X.shape[0]+i2)/(X.shape[0]*Xtest.shape[0])*100, "%")
#         cats = set(list(map(lambda x: Y[x,0], max_sim_indexes)))
#         if Ytest[i1,0] not in cats:
#             errors += 1
#             print("errors: ", errors/(i1+1)*100, "%")
#     return 




if __name__ == "__main__":
    xtrain, xtest, ytrain, ytest = process()
    X, Y, index_to_word, word_to_index = make_vectors(xtrain, ytrain)
    Xtest, Ytest = make_test_vectors(xtest,ytest, word_to_index) 
    pooled_test(X, Y, Xtest, Ytest)
