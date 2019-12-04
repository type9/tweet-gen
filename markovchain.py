from dictogram import Dictogram

class Node(Dictogram):
    def __init__(self, word):
        super(Node, self).__init__()
        self.word = word # the word that this node represents
        self.status = str()
    
    def walk(self): 
        '''chooses a node to walk to based off of sample'''
        return self.sample()

class MarkovChain():
    def __init__(self, text, order):
        self.order = order # number of orders to generate the chain with
        self.nodes = self.generate_nodes(text)
        self.heads = self.generate_heads(text)
    
    def get_phrase(self, text, index):
        phrase = str() # represent the n words seperated by spaces   
        is_first = True 
        for extra_word in range(self.order): # generates the 'phrase' based off of the order which dictates the number of words we look at
            this_word = None # stores the word we're currently looking at

            try: # catches index out of bounds and breaks the loop if out of bounds (means we're at end of text)
                this_word = text[index + extra_word]
            except IndexError:
                return None
            
            if this_word:
                if not is_first: # if it's not the first word in the phrase we add a space before we concetanate the new word
                    phrase += ' '
                    phrase += this_word
                else:
                    phrase = this_word
                    is_first = False

        return phrase
    
    def generate_heads(self, text):
        dictogram = Dictogram()

        for this_word in range(len(text)): # for the length of the text, generate a phrase from each word and store it in a dictogram
            this_phrase = self.get_phrase(text, this_word)
            if this_phrase: # checks for a null value from get_phrase because we're reaching the end of the text
                dictogram.add_count(this_phrase)

        return dictogram

    def generate_nodes(self, text):
        '''iterates across list of words creating a list of nodes'''
        nodes = {} # seperate list to keep track of nodes we've already added and their respective object

        for this_word in range(len(text)): # for each first word in the text we're analysing
            this_phrase = self.get_phrase(text, this_word)
            next_phrase = self.get_phrase(text, this_word + 1)

            if this_phrase: # checks that both are not null
                if this_phrase in nodes.keys(): # if the phrase has already been added as a key
                    if next_phrase:
                        nodes[this_phrase].add_count(next_phrase) # add a token of the next phrase
                else:
                    nodes[this_phrase] = Node(this_phrase) # if not we create a new node
                    if next_phrase:
                        nodes[this_phrase].add_count(next_phrase) # add a token of the next word

        return nodes
    
    def generate_sentence(self, num_words):
        '''generates a sentence with max-length (n) of words'''
        sentence = str()

        this_word = self.heads.sample() # samples text histogram in order to find a lead node
    
        for i in range(num_words):
            sentence += this_word # word gets appended onto the sentence

            if self.nodes[this_word].types == 0: # checks if we're at a end node
                return sentence

            if not i == num_words: # if we're not on the last word
                sentence += ' ' # adds a space

            this_word = self.nodes[this_word].walk() # samples the current node for the next word

        return sentence
        

def main():
    import sys
    arguments = sys.argv[1:]

    my_chain = MarkovChain(arguments, 2)
    print(my_chain.nodes)
    print(my_chain.heads)
    print(my_chain.generate_sentence(5))

if __name__ == '__main__':
    main()