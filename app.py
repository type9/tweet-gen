import os
from flask import Flask, render_template, request, redirect, url_for
from dependencies.tweet_markov_gen import TweetMarkovGen

app = Flask(__name__, static_url_path='')

default_handle = 'elonmusk'
default_order = 2

default_gen = TweetMarkovGen()
default_gen.gen_markov(f'{default_handle}_tweets.json', default_order)

@app.route('/')
def index():
    return default_gen.gen_sentence()

@app.route('/<handle>')
def custom_gen():
  pass

if __name__ == '__main__':
  app.run(debug=True)