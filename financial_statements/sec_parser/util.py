## MAKE THIS A CLASS (MAYBE PARENT AND SUBCLASS - SEC_SENTIMENT(SecHandler(object)))
import nltk
import requests
from bs4 import BeautifulSoup
import numpy as np

from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ratelimit import limits, sleep_and_retry
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

class SecHandler:

    """This class handlers anything to do with downloading SEC data to be used for analysis."""

    # our call limit for SEC Edgar data base
    SEC_CALL_LIMIT = {'calls': 10, 'seconds': 1}

    # avoiding the call limit to edgar database
    @staticmethod
    @sleep_and_retry
    @limits(calls=SEC_CALL_LIMIT['calls'])
    def _call_sec(url):
        return requests.get(url)

    def get(self, url):
        return self._call_sec(url).text

    # def get_sec_data(cik, doc_type, start=0, count=60, date='2018-01-01'):
    #     """
    #     Function downloads SEC file data

    #     :param cik:
    #     :param doc_type:
    #     :param start:
    #     :param count:
    #     :param data: Newest Pricing data date
    #     :return entries:
    #     """
    #     new_price_data = pd.to_datetime(date)
    #     url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany' \
    #         '&CIK={}&type={}&start={}&count={}&owner=exclude&output=atom'.format(cik, doc_type, start, count)
    #     sec_data = SecHandler()..get(url)

    #     feed = BeautifulSoup(sec_data.encode('ascii'), 'xml').feed
    #     entries = [
    #         (
    #             entry.content.find('filing-href').getText(),
    #             entry.content.find('filing-type').getText(),
    #             entry.content.find('filing-date').getText())

    #         for entry in feed .find_all('entry', recursive=False)
    #         if pd.to_datetime(entry.content.find('filing-date').getText()) <= new_price_data]

    #     return entries

    # def get_document_type(doc):
    # """ Returns the document type in lowecase ascii.  This can be used to filter out documents that are not being looked for

    # :param doc: (str) Document string
    # :return doc_type: The Document type lowercased
    # """
    # return None

def remove_html_tag(text):
    """
    Removes the html tags from the text to clean the data

    :param text: (str) The text document

    :return text: (str) Returns the text document free of html tags
    """

    text = BeautifulSoup(text, 'html.parser').get_text()

    return text

def clean_text(text):
    """
    Cleans the text by using various functions passed.

    :param text: (str) The unprocessed text data

    :return text: (str) Returns text document after various preprocessing methods have been applied (html & lowercase)
    """

    text = text.lower()
    text = remove_html_tag(text)

    return text

def get_document_type(doc):
    """
    Returns the type of document in lower case

    :param doc: (str) The document string

    :return doc_type: (str) Document type lowercase
    """

    type_pattern = re.compile(r'<TYPE>\S+')
    match = next(type_pattern.finditer(doc))

    return doc[match.start()+6:match.end()].lower()

def lemmatize_words(words):
    """
    Lemmatize words (assign the same value to words that have many inflections)

    :param words: (List) List of (str) inflections
    :return lemmatized_words: (List) Returns a list of (str) (lemmatized words)
    """

    return [WordNetLemmatizer().lemmatize(word, pos="v") for word in words]

def get_bag_of_words(sentiment_words, docs):
    """
    Calculates the bag of words (total number of 'sentiment' words) present in a document

    :param sentiment_words: (str)
    :param docs: (str)

    :return bag_of_words: 2-D Numpy Ndarray of int (first dimension: document, second dimension: the word)
    """

    # TODO: Implement
    # vectorizer = CountVectorizer(vocabulary=sentiment_words)
    # return vectorizer.fit_transform(docs).toarray()

    # alternatively:
    bag_of_words = np.zeros([len(docs), len(sentiment_words)], dtype=int)
    for i, words in enumerate(docs):
        words_count = Counter(words.split())
        for j, word in enumerate(sentiment_words):
            bag_of_words[i,j] = words_count[word]

    return bag_of_words

def get_cosine_similarity(tfidf_matrix):
    """
    Get cosine similarities for each neighboring TFIDF vector/document

    :param tfidf_matrix:

    :returns:
    """

    # TODO: Implement
    # cosine_similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[1:])
    #print(cosine_similarities)
    # return list(cosine_similarities[0])

    # alternatively:
    cosine_similarities = []
    for i in range(tfidf_matrix.shape[0] - 1):
        u = tfidf_matrix[i:i+1]
        v = tfidf_matrix[i+1:i+2]
        cosine_similarities.append(cosine_similarity(u,v).squeeze())

    return cosine_similarities

def get_jaccard_similarity(bag_of_words_matrix):
    """
    Return jaccard similarities for neighboring documents

    :param bag_of_words_matrix: (2-D Numpy Ndarray of int)

    :return jaccard_similarities: (List of Float) Jaccard Similarities of neighboring documents
    """

    bag_of_words_matrix_bool = bag_of_words_matrix.astype(bool)
    jaccard_similarities = []
    for i in range(bag_of_words_matrix.shape[0] - 1):
        u = bag_of_words_matrix_bool[i]
        v = bag_of_words_matrix_bool[i+1]
        jaccard_similarities.append(jaccard_score(u,v))

    return jaccard_similarities

def get_tfidf(sentiment_words, docs):
    """
    Generate TFIDF values from documents for a certain sentiment

    :param sentiment_words: (Pd.Series) Words that signify a specific sentiment
    :param docs: (List of Str) List of documents used to generate bag of words

    :return tfidf: (2-D Numpy Ndarray of float) TFIDF sentiment for each document
    """

    # TODO: Implement
    # vectorizer = TfidfVectorizer(vocabulary=sentiment_words)
    # return vectorizer.fit_transform(docs).toarray()

    # alternatively:
    N = len(docs)
    idf = []
    for word in sentiment_words:
        freq = sum([ word in d for d in docs])
        idf.append( N/freq )
    all_tf_idfs = []
    for doc in docs:
        freq = Counter(doc.split())
        avg = np.mean([freq[w] for w in sentiment_words])
        doc_tf_idfs = []
        for i, word in enumerate(sentiment_words[::-1]):
            tf = freq[word] / avg if avg else 0.
            doc_tf_idfs.append(tf * idf[i])
        doc_tf_idfs = np.array(doc_tf_idfs)
        l2_norm = np.linalg.norm(doc_tf_idfs)
        if l2_norm != 0.:
            doc_tf_idfs = doc_tf_idfs / l2_norm
        all_tf_idfs.append(doc_tf_idfs)

    return np.array(all_tf_idfs)

def print_ten_k_data(ten_k_data, fields, field_length_limit=50):
    """
    Prints the data of the downloaded documents

    :param ten_k_data: (str) The document data
    :param fields: The 'key' you want to print
    :param field_length: The length of the key

    :return: Prints the downloaded filing documents
    """

    indentation = '  '

    print('[')
    for ten_k in ten_k_data:
        print_statement = '{}{{'.format(indentation)
        for field in fields:
            value = str(ten_k[field])

            # show the return lines
            if isinstance(value, str):
                value_str = '\'{}\''.format(value.replace('\n', '\\n'))
            else:
                value_str = str(value)

            # cut the string if it gets too long
            if len(value_str) > field_length_limit:
                value_str = value_str[:field_length_limit] + '...'

            print_statement += '\n{}{}: {}'.format(indentation * 2, field, value_str)

        print_statement += '},'
        print(print_statement)
    print(']')

