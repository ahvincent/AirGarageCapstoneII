#!flask/bin/python
from flask import Flask, jsonify
import requests
import csv
from textblob import TextBlob

app = Flask(__name__)

data = requests.get("https://storage.googleapis.com/airgarage/parking-tweets.csv")
lines = data.content.splitlines()
document = [line.decode().split(",") for line in lines]
tweets = [row[1] for row in document if len(row) > 2 and row[2] == 'Berkeley']

uniqueTweets = set(tweets)
uniqueTweetsList = list(uniqueTweets)

results = []

for tweet in uniqueTweetsList:
	result_pair = (tweet, TextBlob(tweet).sentiment.polarity)
	results.append(result_pair)

sortedTweets = sorted(results, key=lambda x: x[1])

@app.route('/tweets/best', methods=['GET'])
def get_best():
    return jsonify({'tasks': sortedTweets[-10:][::-1]})

@app.route('/tweets/worst', methods=['GET'])
def get_worst():
    return jsonify({'tasks': sortedTweets[:10]})

if __name__ == '__main__':
    app.run(debug=True)