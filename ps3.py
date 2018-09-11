# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : jdavv
# Collaborators : <your collaborators>
# Time spent    : start:9/7/18

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # Create a list to store each letter that will be iterated over and total_score as 0 we add to this
    letter_values = []
    word_letter_point_sum = 0
    word_length = 0

    # iterate over each char in word, use char as key and append its value to word points
    for char in word.lower():
        word_length += 1
        if char in SCRABBLE_LETTER_VALUES:
            letter_values.append(SCRABBLE_LETTER_VALUES[char])

    # Calculate the sum of letters in word
    word_letter_point_sum = sum(letter_values)

    # Calculate second component of the score
    word_length_points = max(1, 7 * len(word) - 3 * (n - len(word)))

    return word_letter_point_sum * word_length_points

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):

        # hack to replace one of the vowels with *
        if i == 1:
            hand['*'] = 1
        else:
            x = random.choice(VOWELS)
            hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    updated_hand = {}
    for char in hand:
        updated_hand[char] = max(0, hand[char] - word.lower().count(char))

    return updated_hand

# Problem #3: Test word validity


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word = word.lower()
    word_freq = get_frequency_dict(word)

    def word_in_list_wildcard(word, word_list):
        '''

        :param word: a string provided as input from user
        :param word_list: a list of possible words
        :return: word_in_list : Boolean, True if any words in possible_words is found in word_list
        '''

        # Only vowels can be substituted, create a string of vowels to iterate
        VOWELS = 'aeiou'
        # Iterate through the vowel string replacing '*' with a vowel
        possible_words = [word.replace('*', vowel) for vowel in VOWELS]
        # Return True if any possible_words are in word_list
        word_in_list = any([possible_words in word_list for possible_words in possible_words])
        return word_in_list

    def word_in_list(word, word_list):

        # Check that word is actually in word_list
        if word in word_list:
            is_word_in_list = True
        else:
            is_word_in_list = False

        return is_word_in_list

    # When word is in word_list, check that hand character frequency - word character frequency is not a -
    # negative number. This ensures user has enough characters to play that word.
    # If not word_in_list() will trigger the logic to handle an '*' calling word_in_list_wildcard()
    if word_in_list(word, word_list):
        for key in word_freq:
            if key == '*':
                continue
            else:
                if hand.get(key, 0) - word_freq.get(key, 0) >= 0:
                    is_valid = True
                else:
                    is_valid = False
                    break
    else:
        if word_in_list_wildcard(word, word_list):
            is_valid = True
        else:
            is_valid = False

    return is_valid

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

    # evaluate how many hands to play from user
    # num_of_hands_to_play = int(input('How many hands would you like to play? ')) - 1
    # Initialize total score variable
    total_score = 0
    round_hand = deal_hand(HAND_SIZE)

    while sum(round_hand.values()) > 0:
        # show user the hand
        display_hand(round_hand)

        # get a word from the user
        word = input("Word to play: ")

        # handle !! input exit the loop
        if word == "!!":
            break
        # input should be a word TODO sanitize inputs
        else:

            # if word in word_list update hand and score
            if is_valid_word(word, round_hand, word_list):
                total_score += get_word_score(word, HAND_SIZE)
                round_hand = update_hand(round_hand, word)
                continue

        # if False
            else:
                print('Sorry', word, 'is not a word')
                round_hand = update_hand(round_hand, word)
                continue

    if word == '!!':
        print('!! Received, ending hand')
        print('-'*60)
    else:
        print('Out of letters, ending hand')
        print('-'*60)

    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#
    # return calculate_handlen(hand)

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    pass  # TO DO... Remove this line when you implement this function
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # get a hand
    hand = deal_hand(HAND_SIZE)

    # Get user input for how many rounds to play
    max_rounds = int(input("How many hands would you like to play? "))

    # Initialize the round_score, and round_counter variable
    round_score = 0
    round_counter = 1

    # Loop until max_rounds is 0
    while max_rounds >= 0:

        # Play the hand
        round_score += (play_hand(hand, word_list))

        # Print hand score to user
        print('Hand', round_counter, 'Score', round_score)
        print('-'*60)

        # Decrease the max_round count and increase the round_counter
        max_rounds -= 1
        round_counter += 1
        continue

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)




