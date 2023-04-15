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
    
#==============================================================================
# start of the game    
#==============================================================================
    
wordlist = load_words()
secret_word = 'apple'
#choose_word(wordlist)
available_guesses=6
available_letters=string.ascii_lowercase
print('Welcome to the game Hangman!')
length=(len(secret_word))
print('I am thinking of a word that is',length,'letters long.')
n=0
warnings=3
guessed_word=''
letters_guessed=''
while n<available_guesses:
    print('You have',available_guesses-n,'guesses left.')
    print('Available letters:',available_letters)
    letter_guessed=input('Please guess a letter:')
    letters_guessed+=letter_guessed
    get_available_letters(letters_guessed)
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
if n==available_guesses:
    print('Sorry, you ran out of guesses. The word was',secret_word)