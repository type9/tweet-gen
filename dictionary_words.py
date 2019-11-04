import random
import sys
from fisheryates_shuffle import shuffle

def random_sentence(num_words):
    dictionary = open('/usr/share/dict/words', 'r')
    dictionary_list = list()

    word_list = list() # final list of words

    num_lines = 0 # total word count
    for line in dictionary: # converts each line of the dictionary to an array
        num_lines += 1
        dictionary_list.append(line.strip()) # slices off new line char and appends

    dictionary.close() # closes dictionary
    
    if num_lines < num_words: # checks edges case that more words are requested than exist in the file
        return False

    rand_indexes = gen_rand_indexes(num_lines, num_words) # generates a random index for the number of random words we need

    for index in rand_indexes: # for each random index generated, append the word at that index
        word = dictionary_list[index]
        word_list.append(word)
    
    return shuffle(word_list)

def gen_rand_indexes(num_lines, num_indexes):
    indexes = list()
    for i in range(num_indexes): # for the number of idexes append a random index
        index = random.randint(0, num_lines)
    return indexes

if __name__=='__main__':
    num_words = sys.argv[1:]

    print(random_sentence(int(num_words[0])))