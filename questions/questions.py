import nltk
import sys

import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    ret = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file), encoding="utf-8") as f:
            ret[file] = f.read()
    return ret

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    word_list = nltk.word_tokenize(document.lower())
    for index, word in enumerate(word_list):
        if word in nltk.corpus.stopwords.words("english") or word in string.punctuation:
            del word_list[index]
    return word_list



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    ret = {}
    for document in documents.keys():
        for word in documents[document]:
            if ret.get(word) != None:
                continue
            else:
                count = 0
                for w_list in documents.values():
                    if word in w_list:
                        count += 1
                ret[word] = math.log(len(documents)/count)
    return ret


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #for each word in query:
    #    calculate tf-idf for each document and sum them
    #    return list of n documents descending ranked by tf-idfs

    file_scores = {}
    for file, words in files.items():
        sum_tfidf = 0
        for q_word in query:
            if q_word in words:
                sum_tfidf += idfs[q_word] * words.count(q_word)
        if sum_tfidf != 0:
            file_scores[file] = sum_tfidf

    output = [k for k, v in sorted(file_scores.items(), key=lambda x: x[1], reverse=True)]
    return output[:n]



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    sen_scores = {}
    for sentence, words in sentences.items():
        sum_idf = 0
        freq = 0
        for q_word in query:
            if q_word in words:
                sum_idf += idfs[q_word]
                freq += 1
        if sum_idf != 0:
            sen_scores[sentence] = (sum_idf, freq/len(words))

    output = [k for k, v in sorted(sen_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    return output[:n]


if __name__ == "__main__":
    main()
