import random
import sys

def rearrange(my_list):

    for i in range(len(my_list)): # for every list element
        temp = my_list[i] # temp preparring for swap

        rand_index = random.randint(0, (len(my_list)-1)) # choose a random index

        my_list[i] = my_list[rand_index] # swap their places
        my_list[rand_index] = temp
    return my_list

if __name__=='__main__':
    words = sys.argv[1:]

    print(rearrange(words))
    
