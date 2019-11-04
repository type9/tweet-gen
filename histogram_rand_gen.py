import text_analysis

def gen_weighted_word(histogram):
    num_words = unique_words(histogram)
    largest_word = str()
    largest_roll = float()

    for x in range(len(histogram)):
        weight = word_frequency(histogram[x][0], histogram)/num_words
        roll