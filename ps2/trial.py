# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 16:16:37 2023

@author: xiaol
"""
#==============================================================================
# functional basic hangman
#==============================================================================
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
   
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    a=0
    for char in secret_word:
        if char not in letters_guessed:
            a+=1
    return(a==0)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word=''
    for char in secret_word:
        if char in letters_guessed:
            guessed_word+=char
        else:
            guessed_word+='_ '
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters=string.ascii_lowercase
    for char in letters_guessed:
        available_letters=available_letters.replace(char,'')
    return available_letters

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    myword=my_word.replace(' ','')
    a=0
    if len(myword)==len(other_word):
        for (n,i) in zip(myword,other_word):
            if n==i:
                pass
            elif n=='_' and i in available_letters:
                pass
            else:
                a+=1
    else:
        a+=1
    return(a==0)



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matches=''
    for w in wordlist:
        if match_with_gaps(my_word, w):
            matches=matches+w+' '
    print('Possible word matches are:\n',matches)
#==============================================================================
# start of the game    
#==============================================================================
    
wordlist = load_words()
secret_word = choose_word(wordlist)
available_guesses=6
available_letters=string.ascii_lowercase
print('Welcome to the game Hangman!')
length=(len(secret_word))
print('I am thinking of a word that is',length,'letters long.')
n=0
warnings=3
letters_guessed=''
guessed_word=''
while n<available_guesses:
    print('You have',available_guesses-n,'guesses left.')
    print('Available letters:',available_letters)
    letter_guessed=input('Please guess a letter:')
    if letter_guessed.isalpha():
        letter_guessed=letter_guessed.lower()
        if letter_guessed in letters_guessed:
            warnings-=1
            print("Oops! You've already guessed that letter. You have",warnings,"warnings left:",guessed_word)
        else:
            letters_guessed+=letter_guessed
            available_letters=get_available_letters(letters_guessed)
            guessed_word=get_guessed_word(secret_word, letters_guessed)
            winning=is_word_guessed(secret_word, letters_guessed)
            if winning:
                print('Congratulations, you won!')
                break    
            else:
                if letter_guessed in secret_word:
                    print('Good guess:',guessed_word)
                elif letter_guessed in ['a','e','i','o','u']:
                    n+=2
                    print('Oops! That letter is not in my word:',guessed_word)
                else:
                    n+=1
                    print('Oops! That letter is not in my word:',guessed_word)
                print('----------------')
    elif letter_guessed=='*':
        my_word=guessed_word
        show_possible_matches(my_word)
    else:
        warnings-=1
        print("Oops! That is not a valid letter. You have",warnings,"warnings left:",guessed_word)
    if warnings==0:
        n+=1
        warnings=3
if n==available_guesses:
    print('Sorry, you ran out of guesses. The word was',secret_word)