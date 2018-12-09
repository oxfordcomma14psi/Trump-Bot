#! python3

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:45:12 2018

ISE 7300 Project

DTMC Text Generation

@author: chris
"""

import re, random



# Read in text.

text_data_file = open('C:\\Users\\chris\\Google Drive\\Fall18\\ISE 7300\\Project\\trump.txt',
                      'r', encoding = 'utf8')
dirty_text= text_data_file.read()
text_data_file.close()

    
# Create regex to exclude garbage
link_regex = re.compile(r'http\S*')
retweet_regex = re.compile(r'RT')
handle_regex = re.compile(r'@')

regex_list = [link_regex, retweet_regex, handle_regex]

text_data = dirty_text
for rgx_match in regex_list:
    text_data = re.sub(rgx_match, '', text_data)


# Split text into wordlist
    
word_list = text_data.split()
# TODO: fix ampersands!


    # create list of starting states (first word in sentence, first word after)
starting_states = []
for i in range(0, len(word_list) - 1):
    if word_list[i][0].isupper() and  word_list[i][-1] != ',' and \
    word_list[i][-1] != '.' and word_list[i][-1] != '!':
        starting_states.append([word_list[i], word_list[i+1]])

 
ending_states = []
for i in range(1, len(word_list)):
    if word_list[i][-1] == '.' or word_list[i][-1] == '!' or \
    word_list[i][-1] == '?':
        ending_states.append([word_list[i-1], word_list[i]])
    # remove duplicates
    
# create list of states that are not starting states
states = []
for i in range(len(word_list) - 1):     # THIS IS REALLY FUCKING SLOW!
    possible_state = [word_list[i], word_list[i+1]]
    #if possible_state not in starting_states:
    states.append(possible_state)

    
starting_states_dict = {}
for state in starting_states:
    if state[0] in starting_states_dict.keys():     # if 1st word exists as key
        starting_states_dict[state[0]].append(state[1]) # add 2nd word as val
    else: # if 1st word doesn't exist in dict
        starting_states_dict[state[0]] = [state[1]]    # add key and val
        
states_dict = {}
for state in states:
    if state[0] in states_dict.keys():
        states_dict[state[0]].append(state[1])
    else:
        states_dict[state[0]] = [state[1]]
        
# encapsulate into function        
# TODO: add sentence length as input parameter
def build_states(token_length):
    states = []
    for i in range(len(word_list - (token_length - 1))):
        possible_state = []
        for j in range(token_length):
            possible_state.append(word_list[j]) # do this work?
    

def make_quote():
    first_pair = random.choice(starting_states)
    sentence = [first_pair]
    min_sentences = 2
    sentence_counter = 0
    while sentence_counter < min_sentences:
        if [sentence[0][-2], sentence[0][-1]] not in ending_states:
            sentence[0].append(random.choice(states_dict[sentence[-1][-1]]))  
        else: 
            sentence_counter += 1
    print(' '.join(sentence[0]))
    
 
        
        
    
def interactive_mode():
    # problems:
        # not witing for continue input before asking for next word
        # not printing properly
    def is_valid(word):
        if word in states_dict.keys():
            return True
        else:
            return False
    
    def get_start_words(current_word):
        probs = {}
        for next_word in starting_states_dict[current_word]:
            if next_word in probs.keys():
                probs[next_word] += 1
            else:
                probs[next_word] = 1
        for next_word in probs.keys():
            probs[next_word] /= len(starting_states_dict[current_word])
        next_words = []
        for i in range(3):
            max_prob = max(probs.values())
            for word in probs.keys():
                if probs[word] == max_prob:
                    next_words.append(word)
                    del probs[word]
                    break
        return next_words
    
    def get_words(current_word):
        probs = {}
        for next_word in states_dict[current_word]:
            if next_word in probs.keys():
                probs[next_word] += 1
            else:
                probs[next_word] = 1
        for next_word in probs.keys():
            probs[next_word] /= len(states_dict[current_word])
        next_words = []
        for i in range(3):
            max_prob = max(probs.values())
            for word in probs.keys():
                if probs[word] == max_prob:
                    next_words.append(word)
                    del probs[word]
                    break
        return next_words
    
    
    valid = False
    while not valid:
        sentence = []
        word = input('Please enter a starting word: ')
        if word in starting_states_dict.keys():
            valid = True
        if not valid:
            print('Invalid word.')
    sentence.append(word)
    print(' '.join(sentence))
    cont = input('Continue? y/n: ')
    if cont == 'n':
         print('Goodbye!')
         return
     # display next 3
    next_words = get_start_words(word)
    print('Choose the next word. \nPossibilities are:')
    print(next_words[0], next_words[1], next_words[2])
    while True:
         valid = False
         while not valid:
             # input: choose word from list
             word = input('Enter the next word: ')
             # is word valid? update flag
             valid = is_valid(word)
             if not valid:
                 print('Invalid word.')
         # append and print
         sentence.append(word)
         print(' '.join(sentence))
         # continue?
         cont = input('Continue? y/n: ')
         if cont == 'n':
             print('Goodbye!')
             return
         # display next 3
         next_words = get_words(word)
         print('Choose the next word. \nPossibilities are:')
         print(next_words[0], next_words[1], next_words[2])
             
            
            
            
    
    
# unnecessary bullshit below
def top_three_words(current_word):
    top_three = []
    probs = get_probs(current_word)
    # handle case where there are no more possibilities
    # current_word in ending_states
    for i in range(3):
        if len(probs.keys()) > 0:
            v = list(probs.values())
            k = list(probs.keys())
            top_three.append(k[v.index(max(v))])
            del probs[top_three[i]]
        else:
            break
    return top_three
        
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

    
def get_start_words(current_word):
    probs = {}
    for next_word in starting_states_dict[current_word]:
        if next_word in probs.keys():
            probs[next_word] += 1
        else:
            probs[next_word] = 1
    for next_word in probs.keys():
        probs[next_word] /= len(starting_states_dict[current_word])
    # create next word list
    next_words = []
    # get top word
    for i in range(3):
        max_prob = max(probs.values())
        for word in probs.keys():
            if probs[word] == max_prob:
                next_words.append(word)
                del probs[word]
                break
    return next_words
    
    
def get_probs(current_word):
    probs = {}
    for next_word in states_dict[current_word]:
        if next_word in probs.keys():
            probs[next_word] += 1
        else:
            probs[next_word] = 1
    for next_word in probs.keys():
        probs[next_word] /= len(states_dict[current_word])
    next_words = []
    for i in range(3):
        max_prob = max(probs.values())
        for word in probs.keys():
            if probs[word] == max_prob:
                next_words.append(word)
                del probs[word]
                break
    return next_words
        
        
def is_valid(word):
    if word in states_dict.keys():
        return True
    else:
        return False
