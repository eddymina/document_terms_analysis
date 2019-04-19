import argparse
import glob
import os
import re
import math


def mkdir(output):
    """
    Make directory if does not already exist.
    :param      output:
    :return:    True if no directory exists, and 'output' was made; else, False.
    """
    if not os.path.exists(output):
        os.makedirs(output)
        return True
    return False


def is_file(path):
    """Wrapper for os.path.is_file"""
    return os.path.isfile(str(path))


def is_dir(path):
    """Wrapper for os.path.isdir"""
    return os.path.isdir(str(path))


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def file_base(filename):
    """Return c for filename /a/b/c.ext"""
    (head, tail) = os.path.split(filename)
    (base, ext) = os.path.splitext(tail)
    return base


def clean_text(s):
    """ Remove non alphabetic characters. E.g. 'B:a,n+a1n$a' becomes 'Banana' """

    s = re.sub("[^a-z A-Z]", "", s)
    s = s.replace(' n ', ' ')
    return s


def clean_corpus(corpus):
    """ Run clean_text() on each sonnet in the corpus

    :param corpus:  corpus dict with keys set as filenames and contents as a single string of the respective sonnet.
    :type corpus:   dict

    :return     corpus with text cleaned and tokenized. Still a dictionary with keys being file names, but contents
                now the cleaned, tokenized content.
    """
    for key in corpus.keys():
        
        # clean each exemplar (i.e., sonnet) in corpus

        # call function provided to clean text of all non-alphabetical characters and tokenize by " " via split()
        corpus[key] = clean_text(corpus[key]).split()

    return corpus


def read_sonnets(fin):
    """
    Passes image through network, returning output of specified layer.

    :param fin: fin can be a directory path containing TXT files to process or to a single file,

    :return: (dict) Contents of sonnets with filename (i.e., sonnet ID) as the keys and cleaned text as the values.
    """

    """ reads and cleans list of text files, which are sonnets in this assignment"""

    if is_file(fin):
        f_sonnets = [fin]
    elif is_dir(fin):
        f_sonnets = glob.glob(fin + os.sep + "*.txt")
    else:
        print('Filepath of sonnet not found!')
        return None


    sonnets = {}
    for f in f_sonnets:
        sonnet_id = file_base(f)
        data = []
        with open(f, 'r') as file:
            data.append(file.read().replace('\n', '').replace('\r', ''))

        sonnets[sonnet_id] = clean_text("".join(data))
    return sonnets


def get_top_k(kv_dict, k=20):
    """
    :param kv_list:    list of key-value tuple pairs, where value is some score or count.
    :param k:          number of key-value pairs with top 'k' values (default k=20)
    :return:           k items from kv_list with top scores
    """
    return sort_dictionary_by_value(kv_dict)[:k]


def sort_dictionary_by_value(dict_in, direction='descending'):
    order_keys = [d[0] for d in sorted(dict_in.items(), key=lambda x: x[1])]

    if direction == 'descending':
        order_keys.reverse()

    ordered = []
    for key in order_keys:
        ordered.append((key, dict_in[key]))
    return ordered


def tf(document):
    """Determine the term frequency of text exemplar (i.e, document)

    :return     (tuple) as (word, frequency) of length = number unique words in document.
    """
    # count the occurrences of each word in the document
    document_tf = {}
    for element in document:
        document_tf[element] = document_tf.get(element, 0) + 1

    return document_tf


def idf(corpus):
    """Determine the inverted document frequency of a corpus.

    :return     (tuple) as (word, frequency) of length = number unique words in document.
    """
    ndocuments = len(corpus)
    # merge words from all documents, while only taking unique set from each documents so each word is only counts once
    corpus_tf = tf(corpus)
    corpus_idf = {}
    for key, value in corpus_tf.items():
        corpus_idf[key] = math.log(ndocuments / value)

    return corpus_idf


def tf_idf(corpus_idf, sonnet_tf):
    """Determine the inverted document frequency of a corpus.

    :return     (tuple) as (word, frequency) of length = number unique words in document.
    """
    sonnet_tfidf = {}
    for key in sonnet_tf.keys():
        sonnet_tfidf[key] = corpus_idf[key] * sonnet_tf[key]

    return sonnet_tfidf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Text Analysis through TFIDF computation',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str,
                        help='Input text file or files.')
    parser.add_argument('-top_k', type=int, default=20,
                        help='top_k words to show')

    parser.add_argument("--tfidf", type=str, default= None, 
        help="Determine the TF IDF of a document w.r.t. a given corpus")

    

    args = parser.parse_args()

    # return dictionary with keys corresponding to file names and values being the respective contents

    corpus = read_sonnets(args.input)
    # corpus = read_sonnets('sample_folder')
    # corpus = read_sonnets('sample_folder/sample_1.txt')


    # # return corpus (dict) with each sonnet cleaned and tokenized for further processing
    corpus = clean_corpus(corpus)


    # # assign 1.txt to variable sonnet to process and find its TF (Note corpus is of type dic, but sonnet1 is just a str)
    # sonnet1 = corpus['1']

    # determine tf of sonnet
    k = args.top_k
    comparing_sonnet = args.tfidf


    print('\nExamining',len(corpus),'documents...\n')

    # TF of entire corpus
    flattened_corpus = [word.lower() for sonnet in corpus.values() for word in sonnet]
    corpus_tf = tf(flattened_corpus)

    corpus_top20 = get_top_k(corpus_tf,k)
    
    print("Corpus TF (Top {}):".format(k))
    print(corpus_top20)

    # IDF of corpus
    corpus_idf = idf(flattened_corpus)
    corpus_tf_ordered = get_top_k(corpus_idf,k)
    # print top 20 to add to report

    print("\nCorpus IDF (Top {}):".format(k))
    print(corpus_tf_ordered)

    print("\nCorpus TFIDF (Top {}):".format(k))
    print(get_top_k(tf_idf(corpus_idf,corpus_tf),k))

    
    if comparing_sonnet != None: 
        comparing_sonnet = comparing_sonnet.rsplit('.',1)[0]
        print("\nCorpus TFIDF Compared to {} (Top {}):".format(comparing_sonnet,k))
        print(get_top_k(tf_idf(corpus_idf,tf([word.lower() for word in corpus[comparing_sonnet]])),k))

    # TFIDF of Sonnet1 w.r.t. corpus
    # sonnet1_tfidf = tf_idf(corpus_idf, sonnet1_tf)
    # sonnet1_tfidf_ordered = get_top_k(sonnet1_tfidf)
    # print
    # print("Sonnet 1 TFIDF (Top 20):")
    # print(sonnet1_tfidf_ordered)
