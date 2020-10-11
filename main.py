# The 6.0001 Word Game

import math
import random
import string
import copy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0}


WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

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



def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

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
    first_component = 0

    for letter in word.lower():
        first_component += SCRABBLE_LETTER_VALUES[letter]
    second_component = (7*len(word)-3*(n-len(word)))
    if second_component < 1:
        second_component = 1
    return first_component*second_component


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()


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
    
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1
    
    return hand


def update_hand(hand, word):
    """

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    hand2 = copy.deepcopy(hand)
    for letter in word.lower():
        if hand2.get(letter, 0) > 0:
            hand2[letter] = hand2[letter] - 1

    for letter in hand.keys():
        if hand2[letter] < 1:
            hand2.pop(letter)
    return hand2


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
    hand2 = copy.deepcopy(hand)
    result = False
    wordlower = word.lower()

    if '*' in wordlower:
        index_wildcard = word.index('*')
        for i in VOWELS:
            if (wordlower[0:index_wildcard] + i + wordlower[index_wildcard+1:]) in word_list:
                result = True
                break
            else:
                result = False
        if not result:
            return False

        for letter in wordlower:
            if letter in hand2.keys():
                result = True
                hand2[letter] = hand2[letter] - 1
                if hand2[letter] == 0:
                    hand2.pop(letter)
            else:
                return False

    else:
        if wordlower in word_list:
            result = True
        else:
            return False
        for letter in wordlower:
            if letter in hand2.keys():
                result = True
                hand2[letter] = hand2[letter] - 1
                if hand2[letter] == 0:
                    hand2.pop(letter)
            else:
                return False
    return result



def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for letter in hand.keys():
        length += hand[letter]
    return length


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * You may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the you to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and you are
        asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      You can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score = 0
    while calculate_handlen(hand) > 0:
        print('Current Hand: ')
        display_hand(hand)
        user_choice = input('Enter word, or "!!" to indicate that you are finished: ')

        if user_choice == "!!":
            break

        else:
            if is_valid_word(user_choice, hand, word_list):

                print('"'+user_choice+'" earned ' + str(get_word_score(user_choice, calculate_handlen(hand))) + 'points')
                total_score += get_word_score(user_choice, calculate_handlen(hand))

                hand = update_hand(hand, user_choice)

            else:
                print('That is not a valid word. Please choose another word.')

    print('Total score for this hand: ' + str(total_score) + ' points')

    return total_score



def substitute_hand(hand, letter):
    """ 
    Allow you to replace all copies of one letter in the hand (chosen by you)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from your choice, and should not be any of the letters
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

    hand2 = copy.deepcopy(hand)
    if letter.lower() in CONSONANTS:
        new_letter = random.choice(CONSONANTS)
        while new_letter in hand.keys() or new_letter == letter.lower():
            new_letter = random.choice(CONSONANTS)
        value = hand2[letter]
        hand2.pop(letter)
        hand2[new_letter] = value
    else:
        new_letter = random.choice(VOWELS)
        while new_letter in hand.keys() or new_letter == letter.lower():
            new_letter = random.choice(VOWELS)
        value = hand2[letter]
        hand2.pop(letter)
        hand2[new_letter] = value

    return hand2

    
def play_game(word_list):
    """
    Allow you to play a series of hands

    * Asks to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, you are asked if you want to substitute
      one letter for another. If 'yes', you are prompted for desired letter.
      This can only be done once during the game.

    * For each hand, you are asked if you would like to replay the hand.
      If 'yes', hand is replayed and
      the better of the two scores is kept.  This can only be done once
      during the game. Replaying the hand does
      not count as one of the total number of hands you initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    num_of_subs = 1
    num_of_hands = int(input('Enter total number of hand: '))
    total_score = 0
    while num_of_hands > 0:
        hand = deal_hand(HAND_SIZE)
        print('Current Hand: ')
        display_hand(hand)
        if num_of_subs > 0:
            make_sub = input('Would you like to substitute a letter? ')
            if make_sub.lower() == 'yes':
                num_of_subs -= 1
                letter_to_sub = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, letter_to_sub)

        score = play_hand(hand, word_list)
        print('---------------')
        replay_hand = input('Would you like to replay the hand? ')
        if replay_hand == 'yes':
            score2 = play_hand(hand, word_list)
            print('---------------')
        elif replay_hand == 'no':
            score2 = 0
        if score > score2:
            total_score += score
        else:
            total_score += score2
        num_of_hands -= 1

    print('Total score over all hands: ' + str(total_score))


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
