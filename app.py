from flask import Flask, request, render_template, jsonify, redirect
import pymongo
import random
from config import dbname, dbuser, psswd, host, parameters
from flask_pymongo import PyMongo

import pandas as pd
import re
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from nltk import tokenize
import nltk

app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(
    app, uri='mongodb+srv://' + dbuser + ':' + psswd + host + '/' + dbname + "?" + parameters)
query = {'#tag': {"$in": ['Greta Thunberg', 'greta',
                          'Greta']}, 'module_sent_an': {"$in": ['1', '0']}}

id_global = ''


def classify_text( text ):
    # Load the model from the file
    filename = './static/models/tweet_model.sav'
    model = pickle.load(open(filename, 'rb'))

    # Read a test file 
    test = pd.read_csv("./static/data/to_test.csv")

    # Remove links 
    text = re.sub(r'https?://\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'http?://\S+', '',  text, flags=re.MULTILINE)
    # Remove ampersand pattern
    text = re.sub('&amp;', '',         text, flags=re.MULTILINE)

    # Remove twitter patterns
    text = re.sub("@[\w]*", '', text, flags=re.MULTILINE)
    text = re.sub("RT :*", '', text, flags=re.MULTILINE)

    # Remove punctuation, numbers, and special characters
    text = re.sub("[^a-zA-Z# ]", '', text, flags=re.MULTILINE)

    # Remove stopwords
    token_space = tokenize.WhitespaceTokenizer()
    stopwords = nltk.corpus.stopwords.words("english")
    new_phrase = list()
    text_words = token_space.tokenize(text.lower())
    for word in text_words:
        if word not in stopwords:
            new_phrase.append(word)
    text = ' '.join(new_phrase)

    # Stemming: Basically transform variation of words like gerund in the root word. 
    from nltk import PorterStemmer   
    ps = PorterStemmer()
    tokens = text.split()
    stemmed_tokens = [ps.stem(token) for token in tokens]
    text = ' '.join(stemmed_tokens)

    # Create the tweet row to predict and add to the first position on the test    
    test.iloc[0] = ['A1', text]

    # Apply the same criteria use to create the model.
    vectorizer = CountVectorizer(lowercase=True, max_features=1300)
    bag_of_words = vectorizer.fit_transform(test['treated'].apply(lambda x: np.str_(x)))
    predited = model.predict(bag_of_words)

    # Returns the text prediction 
    return str(predited[0])


@app.route('/twitter')
def twitter():
    query_custom = {'#tag': {"$in": ['Greta Thunberg', 'greta',
                                     'Greta']}}
    docs = []
    for doc in mongo.db.twitter.find(query_custom):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)


@app.route('/getnewtwitter')
def getnewtwitter():
    query_custom = {'#tag': {"$in": ['Greta Thunberg', 'greta',
                                     'Greta']}}
    docs = []
    for doc in mongo.db.twitter.find(query_custom):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)

@app.route('/predict', methods=["POST"])
def predict():

    # Get the tweet
    tweet = request.form['tweet']
    # Call function to clasify the tweet
    to_return = classify_text(tweet)

    # Check the classification
    sentiment = to_return
    if (to_return == '0'):
        sentiment += ' - Sentiment Negative'
    else: 
        sentiment += ' - Sentiment Positive'

    result = {'prediction': sentiment}
    result['text'] = tweet
    result['textblob'] = request.form['textblob']
    result['module_sent_an'] = request.form['human']

    return render_template("index.html", result=result)

@app.route('/label')
def label():
    docs = []
    for doc in mongo.db.twitter.find(query):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)


@app.route('/plot')
def plot():
    return render_template("plot.html")

@app.route('/')
def index():
    # retrieving a random text from twitter and get a random message based on the query
    count = mongo.db.twitter.find(query).count()
    result = mongo.db.twitter.find(query)[random.randrange(count)]
    result['prediction'] = ''
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", result=result)

@app.route("/filterLessRange_IG_Rank/<value>")
def filterRankRange(value):
    # return items from a different collection (international_gross_det) base on the rank
    value = int(value)
    docs = []
    # select data less or equal the rank selected
    for doc in mongo.db.international_gross_det.find({'rank': {'$lte': value}}):
        doc.pop('_id')
        docs.append(doc)
    return jsonify(docs)

@app.route('/predictinput')
def predictinput():

    result = {'text': 'Type your text here'}
    result['img'] = 'NEUTRAL'

    return render_template("predict-input.html", result=result)

@app.route('/predicttext', methods=["POST"])
def predicttext():

    # Get the text
    text = request.form['text']

    # Call function to clasify the tweet
    to_return = classify_text(text)

    img = ''
    if (to_return == '0'):
        img = 'NEGATIVE'
    else: 
        img = 'POSITIVE'

    result = {'text': to_return}
    result['img'] = img

    return render_template("predict-input.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
