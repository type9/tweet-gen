import random
import sys

def shuffle(array):
    back_index = len(array) -1 

    for elem in array: # for each element in array
        rand_index = random.randint(0, back_index) # generate random index spanning first index to last unshuffled index

        temp = array[back_index] # store back most (unshuffled) element
        array[back_index] = array[rand_index] # swap their places with randomly generated index
        array[rand_index] = temp

        back_index -= 1 # deincrement back index

    return array

if __name__=='__main__':
    array = sys.argv[1:]

    print(shuffle(array))