import numpy as np
import pandas as pd
# TF-IDF


def freq_normal(lst, dic) :
    ctot = len(lst)
    for w in set(lst) :
        cw = lst.count(w)
        if w in dic:
            dic[w].append(cw / ctot)
        else :
            dic[w] = [cw / ctot]
            
def freq_log(lst, dic, factor = 100) :
    """
    factor for changing ratio between 1 and freq
    """
    ctot = len(lst)
    for w in set(lst) :
        cw = lst.count(w)
        if cw in dic:
            dic[cw].append(np.log(1 + factor * cw / ctot))
        else :
            dic[cw] = [np.log(1 + factor * cw / ctot)]
            
def freq_k(lst, dic, K=0.5) :
    """
    K in [0, 1]
    """
    ctot = len(lst)
    lst_set_w = list(set(lst))
    lst_cnt = list(map(lambda x: lst.count(x), lst_set_w))
    maxi = np.max(lst_cnt)
    lst_cnt = K + (1-K) * np.array(lst_cnt) / maxi
                       
    for (w, f) in zip(lst_set_w, lst_cnt) :
        if w in dic:
            dic[w].append(np.log(1 + factor * cw / ctot))
        else :
            dic[w] = [np.log(1 + factor * cw / ctot)]

def frequency(lst, dic, method = "normal", K = 1):
    """
    lst: list of words preprocessed
    dic: where will be stored the frequency info
    method: normal |  log | K max
    """
    if method == "normal" :
        freq_normal(lst, dic)
    elif method == "log" :
        freq_log(lst, dic, K)
    elif method == "K" and K <=1 and K >= 0:
        freq_k(lst, dic, K=K)    
    else :
        print("Parameters bug")
        freq_normal(lst, dic)

        
def idf(dic, ndoc, method="normal") :
    """
    method: normal | smooth | max | proba
    NB: there is always a "1+" for logs. Avoid non positive TF
    """
    CNT = np.array(list(map(lambda x: len(dic[x]), dic)))
    
    if method == "normal" :
        return np.log(ndoc/CNT)
    elif method == "smooth":
        return np.log(1+ ndoc/CNT)
    elif method == "max":
        CNT = 1 + CNT
        maxi = CNT.max()
        return np.log(maxi / CNT)
    elif method == "proba":
        return np.log((ndoc - CNT)/CNT)
    else:
        print("Parameters bug")
        return np.log(ndoc/CNT)
    