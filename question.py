import requests
import re
import datetime

import numpy as np
import pandas as pd


def create_query(search_query, where="all", start=0, max_results=10, sortBy="submittedDate", sortOrder="descending"):
    """
    search_query: terms of the research, spaces with OR AND ANDNOT 
    (TODO: update this to submit thing according to arXiv format)
    where: all | tl | cat | ... see the documentation
    maxResults: default 10, max 30000
    sortBy: relevance | lastUpdatedDate | submittedDate
    sortOrder: ascending | descending
    """
    
    return """http://export.arxiv.org/api/query?search_query={}:{}&sortBy={}&sortOrder={}&start={}&max_results={}""".format(where, 
                                                                                search_query, 
                                                                                sortBy, 
                                                                                sortOrder,
                                                                                start,
                                                                                max_results)

def launch_query(url):
    response = requests.get(url)
    return response.content.decode()



ID_MAIN                = '<id>http://arxiv.org.api/[a-zA-Z0-9 .!:;,?]+</id>'
OPENSEARCH_TOT_RESULTS = '<opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">[0-9]+</opensearch:totalResults>'
UPDATED                = "<updated>[0-9\-A-Z:]+</updated>"
PUBLISHED              = "<published>[0-9\-A-Z:]+</published>"
TITLE                  = "<title>[a-zA-Z0-9 .!:;,?]+</title>"
AUTHOR_NAME            = "<author>[ \n]+<name>[a-zA-Z0-9 .!:;,?]+</name>[ \n]+</author>"
CATEGORY               = '<category term=[a-zA-Z0-9 .!:;,?"]+ scheme="http://arxiv.org/schemas/atom"/>'

re_id        = re.compile(ID_MAIN)
re_max       = re.compile(OPENSEARCH_TOT_RESULTS)
re_title     = re.compile(TITLE)
re_author    = re.compile(AUTHOR_NAME) # unsafe
re_published = re.compile(PUBLISHED)
re_updated   = re.compile(UPDATED)
re_category  = re.compile(CATEGORY) 


re_entry_start = re.compile('<entry>')
re_entry_end   = re.compile('</entry>')
re_summary_start = re.compile('<summary>')
re_summary_end   = re.compile('</summary>')



def get_main_id(lst):
    return list(map(lambda x: x[25:-6], lst))

def get_max_results(lst):
    return list(map(lambda x: int(x[81:-26]), lst))

def get_published(lst):
    return list(map(lambda x: datetime.datetime.strptime(x[11:-12], "%Y-%m-%dT%H:%M:%SZ"), lst))

def get_title(lst):
    return list(map(lambda x: x[7:-8], lst))

def get_author(lst):
    return list(map(lambda x: x[21:-21], lst))

def get_category(lst):
    return list(map(lambda x: x[15:-41], lst))



def extract_spe(txt, re_start, re_end):
    lst = []
    for g1, g2 in zip(re_start.finditer(txt), re_end.finditer(txt)):
        lst.append(txt[g1.end(): g2.start()])
    return lst

def extract_entry(txt):
    return extract_spe(txt, re_entry_start, re_entry_end)

def extract_summary(txt):
    return extract_spe(txt, re_summary_start, re_summary_end)

def extract_main_id(txt):
    return get_main_id(re_id.findall(txt))

def extract_max_results(txt, single = True):
    """
    Search the number of results.
    If one query, must be one unique result
    """
    lst_max = get_max_results(re_max.findall(txt))
    if single :        
        return lst_max[0] if lst_max != [] else 0
    else :
        return lst_max

def extract_author(txt):
    return get_author(re_author.findall(txt))

def extract_title(txt):
    return get_title(re_title.findall(txt))

def extract_category(txt):
    return get_category(re_category.findall(txt))


def preprocessing(txt):
    """
    Convert string
    to list of string
    """
    lst_words = txt.lower()
    while '{' in lst_words :
        c1 = lst_words.find("{")
        c2 = lst_words.find("}")
        if c2 > c1 :
            lst_words = lst_words[:c1] + lst_words[c2+1:]
        elif c2 == -1 :
            # please, no typo
            lst_words = lst_words[:c1] + lst_words[c1+1:]
        else : 
            lst_words = lst_words[:c2] + lst_words[c2+1:]

    for m in """,;:!'"?./_()[]$&\\+1234567890~`""" :
        lst_words = lst_words.replace(m, " ")
    return lst_words
    

def empty_dic(lst, dic):
    return

    
def iterator_query(keywords, process_lst, process_dic=empty_dic, STEP_SIZE = 100, maxn=2000):
    """
    keyword: content of the query
    process: function to apply on everything of the answer content, generally extract + do something
    """
    url = create_query(keywords)
    rep = launch_query(url)
    nmax = extract_max_results(rep)
    print("Number of item {} / {}".format(nmax, maxn))
    nmax = min(nmax, maxn)
    
    lst = []
    dic = {}
    
    nsteps = int(nmax/STEP_SIZE) + 1
    print("Number of item: {}\nNumber of steps to perform: {}; size: {}".format(nmax, nsteps, STEP_SIZE))

    
    for i in range(nsteps) :
        st = STEP_SIZE * i
        en = min(STEP_SIZE * (i+1), nmax)
        delta = en - st
        if delta <= 0 :
            break

        print("Step {}".format(i))
        
        my_url = create_query(keywords, max_results = delta, start = st, sortOrder="ascending")
        Result = launch_query(my_url)
        
        lst = process_lst(Result)
        process_dic(lst, dic)
        
    print("Finished !")
    return nmax, lst, dic