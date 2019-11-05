import sys
import random

class Histogram():
    def __init__(self, word_list=None):
        self.histogram = self.make_histogram(word_list)
        self.total_words = int()
        self.unique_words = int()

    def make_histogram(self, word_list):
        ''' takes a list of words, counts the words and returns a 
            list in the format ['word', int(word_count)]'''

        word_count = list()

        for word in word_list: # for each word in our list of words
            word_in_list = False

            for x in range(len(word_count)): # loop through our running word_count
                if word_count[x][0] == word: # if an element already has that word
                    word_count[x][1] += 1 # increment the count by one
                    word_in_list = True # mark that we've found the word in our list
        
            if not word_in_list: # if we didn't find it in that loop, append a new word with a count of 1
                word_count.append([word, 1])

        return  word_count

    def count_unique_words(self):
        '''takes a histogram in the format ['word', int(word_count)] and
            returns number of unique words'''

        unique_word_count = len(self.histogram) # takes the length of each entry in the histogram

        self.unique_words = unique_word_count

    def word_frequency(self, word):
        '''takes a histogram in the format ['word', int(word_count)] and
            a word, and returns the associated word count. If it can't find
            the word, it returns false'''
        
        for i in range(len(self.histogram)): # loop through histogram
            if self.histogram[i][0] == word: # if we find the word
                return self.histogram[i][1] # return the associated word_count
        
        return False # if the word was not found we return false
    def count_word_total(self):
        '''counts total words in histogram'''
        count = 0
        for i in range(len(self.histogram)):
            count += self.histogram[i][1]
        self.total_words = count

    def sample_by_frequency(self):
        self.count_word_total()
        total_words = self.total_words
        target = random.randint(0, (self.total_words - 1)) # generates a target integer to find

        last_word = str()
        running_count = 0
        for word in range(total_words):
            last_word = self.histogram[word][0]
            running_count += self.histogram[word][1]
            if running_count > target: # if we have passed the target with our count, we return the last word we used
                return last_word

def test_sample(histogram):
    sample_size = 100000
    sample = list()

    for i in range(sample_size):
        word = histogram.sample_by_frequency()
        sample.append(word)
    
    sample_histogram = Histogram(sample)

    sample_histogram.count_unique_words()
    sample_histogram.count_word_total()
    histogram.count_unique_words()
    histogram.count_word_total()

    print(sample_histogram.unique_words)
    print(sample_histogram.histogram)

    for i in range(sample_histogram.unique_words):
        word = sample_histogram.histogram[i][0]

        exp_freq = histogram.word_frequency(word)/histogram.total_words
        act_freq = sample_histogram.word_frequency(word)/sample_histogram.total_words

        print(f'[{i}]{word}: Expected Frequency = {exp_freq}, Actual Frequency = {act_freq}')

if __name__=='__main__':
    array = sys.argv[1:]

    my_histogram = Histogram(array)
    print(my_histogram.histogram)

    test_sample(my_histogram)