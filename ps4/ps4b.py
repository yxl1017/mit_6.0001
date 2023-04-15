# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
valid_words = load_words(WORDLIST_FILENAME)

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = valid_words

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy = self.valid_words.copy()
        return copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        upper = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        shift_dict = {}
        for letter in upper:
            if upper.index(letter) + shift < 26:
                new_letter = upper[upper.index(letter) + shift]
            else:
                new_letter = upper[upper.index(letter) + shift - 26]
            shift_dict[letter] = new_letter
            
        for letter in lower:
            if lower.index(letter) + shift < 26:
                new_letter = lower[lower.index(letter) + shift]
            else:
                new_letter = lower[lower.index(letter) + shift - 26]
            shift_dict[letter] = new_letter
            
        return shift_dict    

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_text = ''
        shift_dict = self.build_shift_dict(shift)
        for char in self.get_message_text():
            if char in string.ascii_letters:
                new_char = shift_dict[char]
            else:
                new_char = char
            shifted_text += new_char
        return shifted_text

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.get_encryption_dict()
        self.message_text_encrypted = self.get_message_text_encrypted()

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        shift = self.get_shift()
        encryption_dict = self.build_shift_dict(shift).copy()
        return encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        shift = self.get_shift()
        return self.apply_shift(shift)

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.get_encryption_dict()
        self.get_message_text_encrypted()


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_validwords = 0
        original_text = ''
        for s in range(26):
            text = self.apply_shift(26 - s)
            number_validwords = 0
            for word in text.split():
                if is_word(valid_words, word):
                    number_validwords +=1
            if number_validwords >= max_validwords:
                max_validwords = number_validwords
                original_text = text
                shift = 26 - s
        return (shift, original_text)

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #story = get_story_string()
    story = 'Nlpdlc hld ly lnnzxawtdspo lfeszc lyo stdezctly ld hpww ld l delepdxly; xfns zq std wtqp td vyzhy qczx std zhy lnnzfyed zq std xtwtelcj nlxaltryd. Zespc nzyepxazclcj dzfcnpd tynwfop esp wpeepcd lyo dappnspd zq Ntnpcz lyo esp stdezctnlw hctetyrd zq Dlwwfde. Wlepc mtzrclastpd zq Nlpdlc mj Dfpezytfd lyo Awfelcns lcp lwdz txazcelye dzfcnpd. Nlpdlc td nzydtopcpo mj xlyj stdezctlyd ez mp zyp zq esp rcplepde xtwtelcj nzxxlyopcd ty stdezcj.[6] Std nzryzxpy hld dfmdpbfpyewj lozaepo ld l djyzyjx qzc "Pxapczc"; esp etewp "Nlpdlc" hld fdpo esczfrszfe esp Czxly Pxatcp, rtgtyr ctdp ez xzopcy opdnpyolyed dfns ld Vltdpc lyo Edlc. Sp sld qcpbfpyewj laaplcpo ty wtepclcj lyo lcetdetn hzcvd, lyo std azwtetnlw astwzdzasj, vyzhy ld Nlpdlctdx, sld tydatcpo azwtetntlyd tyez esp xzopcy pcl.'
    ciphertext = CiphertextMessage(story)
    print(ciphertext.decrypt_message())