import re
import nltk

from markovchain import MarkovChain

from nltk.tokenize import sent_tokenize, TweetTokenizer

from bs4 import BeautifulSoup

from twitterscraper import query_tweets_from_user

class TweetMarkovGen():
    def __init__(self, user_handle, sample_size=100, markov_order=2, output_corpus=False, output_path='corpus.txt'):
        self.user = user_handle

        self.sample_size = sample_size
        self.sample = None

        self.markov_order = markov_order

        self.output_corpus = output_corpus
        self.output_path = output_path

        # CONFIG
        self.STARTTOKEN = '!START'
        self.STOPTOKEN = '!END'

        # Instantiation
        self.chain = MarkovChain(order=markov_order, starttoken=self.STARTTOKEN, stoptoken=self.STOPTOKEN)
    
    def get_tweets(self):
        self.sample = query_tweets_from_user(self.user, self.sample_size)
        print(self.sample)

    def remove_urls(self, text):
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        return text

    def clean_sample(self, sample):
        final = str()

        print(f'BEFORE CLEAN: {sample}')

        sample = BeautifulSoup(sample, features='lxml') # converts sample into a BS4 object
        final = sample.get_text()
        final = self.remove_urls(final)

        print(f'AFTER CLEAN: {final}')
        return final

    def add_startstop(self, sentence):
        '''Adds start and stop token begnning and end of the sentence'''
        sentence.insert(0, self.STARTTOKEN)
        sentence.append(self.STOPTOKEN)
        return sentence
    
    def parse_tweet(self, tweet):
        tokenizer = TweetTokenizer()

        tweet_text = self.clean_sample(tweet.text) # cleaning sample text for parsing

        sentences = sent_tokenize(tweet_text) # breaks into sentences
        for sentence in sentences: # for each sentence
            this_sentence = []
            this_sentence = tokenizer.tokenize(sentence) # tokenize according to nltk tweet tokenizer
            this_sentence = self.add_startstop(this_sentence) # add start and stop tokens
            self.chain.gen_nodes(this_sentence) # add those nodes to the chain
    
    def gen_markov(self):
        self.get_tweets()

        for tweet in self.sample:
            self.parse_tweet(tweet)
    
    def gen_sentence(self):
        sentence = str()

        self.gen_markov()
        sentence = self.chain.gen_sentence()

        return sentence

def main():
    import sys
    arguments = sys.argv[1:]

    user = arguments[0]
    sample_size = int(arguments[1])
    order = int(arguments[2])

    my_markov = TweetMarkovGen(user, sample_size, order)
    print(my_markov.gen_sentence())

if __name__ == '__main__':
    main()

    