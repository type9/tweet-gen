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
    def __init__(self, order=2, starttoken='!START', stoptoken='!STOP'):
        self.order = order # number of orders to generate the chain with

        self.nodes = dict()

        self.STARTTOKEN = starttoken
        self.STOPTOKEN = stoptoken
    
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

    def gen_nodes(self, text):
        '''iterates across list of words creating or modifying nodes'''
        for this_word in range(len(text)): # for each first word in the text we're analysing
            this_phrase = self.get_phrase(text, this_word)
            next_phrase = self.get_phrase(text, this_word + 1)

            if this_phrase: # checks that both are not null
                if this_phrase in self.nodes.keys(): # if the phrase has already been added as a key
                    if next_phrase:
                        self.nodes[this_phrase].add_count(next_phrase) # add a token of the next phrase
                else:
                    self.nodes[this_phrase] = Node(this_phrase) # if not we create a new node
                    if next_phrase:
                        self.nodes[this_phrase].add_count(next_phrase) # add a token of the next phrase
    
    def gen_sentence(self):
        '''generates a sentence with max-length (n) of words'''
        sentence = str()

        this_word = self.nodes[self.STARTTOKEN].walk() # start with the start token
    
        while not this_word == self.STOPTOKEN: # while we don't run into a stop token

            sentence += this_word + ' ' # word gets appended onto the sentence

            this_word = self.nodes[this_word].walk() # samples the current node for the next word

        return sentence
        

def main():
    import sys
    arguments = sys.argv[1:]

if __name__ == '__main__':
    main()