# ===========================
# Functions for preprocessing
# ===========================

import re
import numpy as np
form sklearn.feature_extraction.text import TfidVectorizer, CountVectorizer

# remove extra values
# removing everthing that is not a regular expression
is_url = re.compile(r'http[s]?:// (?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', re.VERBOSE | re.IGNORECASE)
is_rt_username = re.compile(r'^RT+[\s]+(@[\w_]+:)',re.VERBOSE | re.IGNORECASE) #r'^RT+[\s]+(@[\w_]+:)'
# removing tags
is_entity = re.compile(r'@[\w_]+', re.VERBOSE | re.IGNORECASE)

# print topics
def print_topics(model, count_vectorizer, n_top_words):
    """
    Prints the topics of the twitter data
    """
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])) 

# show top n keywords for each of the topics
def show_topics(vectorizer, lda_model, n_words=20):
    """
    Show the topcs and the most common keywords
    """
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))

    return topic_keywords
     
        
def clean_tweet(row):
    """
    Clean the tweets of urls, usernames, and excess words
    """
    row = is_url.sub("",row)
    row = is_rt_username.sub("",row)
    row = is_entity.sub("",row)

    return row

def tokenize_only(text):
    """
    Toeknize the tweets (Sentence -> words) and filter any numerical tokens
    """
    # tokenize by sentence,then word
    tokens = [word.lower() for sent in tok.sent_tokenize(text) for word in tok.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)

    return filtered_tokens