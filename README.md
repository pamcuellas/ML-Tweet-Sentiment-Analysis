## Machine Learning - Tweet Sentiment Analysis

This application applies Sklearn Logistic Regression to classify tweets text in positive or negative. The subject is the speech of Greta Thunberg about climate change done on September 23, 2019, on the United Nations. The application also classifies the tweets in political or not political.
The initial dataset used by this application is a result of consuming Twitter Rest API. It has 1057 tweets and was classified manually to be the base of our model. After that, we added the Python library TextBlob to compare its classification with the human and model classifications.

To replicate this project you will need to create a MongoDB database, a twitter developer account to get the credentials to use the tweepy and searchtweets libraries, and finally write this information on the config.py and search_tweets_creds_example.yaml files.

A list of technologies used are flask, pymongo, pickle (to save and load the model), sklearn, nltk, pandas, re (to clean up the data), tweepy (to use the Twitter API), searchtweets, seaborn, word cloud, and matplotlib; HTML5, CSS3, jQuery, Plotly, D3, Bootstrap, MongoDB, JSON, and Tableau.

### To check out this application online access https://ml-tweet-sentiment-analysis.herokuapp.com/


