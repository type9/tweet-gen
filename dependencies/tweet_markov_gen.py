import datetime as dt
import collections
import re
import nltk
import json

from dependencies.tuple_markovchain import MarkovChain

from nltk.tokenize import sent_tokenize, TweetTokenizer

from bs4 import BeautifulSoup

from twitterscraper import query_tweets_from_user

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, collections.Iterable):
            return list(obj)
        elif isinstance(obj, dt.datetime):
            return obj.isoformat()
        elif hasattr(obj, '__getitem__') and hasattr(obj, 'keys'):
            return dict(obj)
        elif hasattr(obj, '__dict__'):
            return {member: getattr(obj, member)
                    for member in dir(obj)
                    if not member.startswith('_') and
                    not hasattr(getattr(obj, member), '__call__')}

        return json.JSONEncoder.default(self, obj)

class TweetMarkovGen():
    def __init__(self):
        # CONFIG
        self.STARTTOKEN = '!START'
        self.STOPTOKEN = '!STOP'

        # Instantiation
        self.chain = None
    
    def get_tweets(self, user, sample_size, output_to_file=True):
        sample = query_tweets_from_user(user, sample_size)

        if output_to_file:
            with open(f'{user}_tweets.json', 'w', encoding='utf-8') as output_file:
                output_file.write(json.dumps(sample, cls=JSONEncoder))
            output_file.close()

        return sample
    
    def remove_urls(self, text):
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        return text

    def clean_sample(self, sample):
        final = str()

        sample = BeautifulSoup(sample, features='lxml') # converts sample into a BS4 object
        final = sample.get_text()
        final = self.remove_urls(final)

        return final

    def add_startstop(self, sentence):
        '''Adds start and stop token begnning and end of the sentence'''
        sentence.insert(0, self.STARTTOKEN)
        sentence.append(self.STOPTOKEN)
        return sentence
    
    def parse_tweet(self, tweet):
        tokenizer = TweetTokenizer()

        tweet_text = self.clean_sample(tweet['text']) # cleaning sample text for parsing

        sentences = sent_tokenize(tweet_text) # breaks into sentences

        for sentence in sentences: # for each sentence
            this_sentence = []
            this_sentence = tokenizer.tokenize(sentence) # tokenize according to nltk tweet tokenizer
            this_sentence = self.add_startstop(this_sentence) # add start and stop tokens
            self.chain.gen_nodes(this_sentence) # add those nodes to the chain
    
    def gen_markov(self, file_path=None, order=2):
        self.chain = MarkovChain(order=order, starttoken=self.STARTTOKEN, stoptoken=self.STOPTOKEN)
        if file_path:
            with open(file_path) as file:
                sample = json.load(file)
                for tweet in sample: 
                    self.parse_tweet(tweet)
    
    def gen_sentence(self):
        return self.chain.gen_sentence()

def main():
    import sys
    arguments = sys.argv[1:]

    user = arguments[0]
    sample_size = int(arguments[1])
    order = int(arguments[2])

    my_markov = TweetMarkovGen()
    my_markov.gen_markov(f'{user}_tweets.json', order)
    sentence = my_markov.gen_sentence()
    print(f'\n{sentence}')

if __name__ == '__main__':
    main()

    