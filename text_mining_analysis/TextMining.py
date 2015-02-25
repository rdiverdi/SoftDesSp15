"""
Turns text file into a madlibs game
1st argument is the name of the text file (from project Gutenberg)

prompts user for parts of speach then prints one
paragraph of the original file in mad-libs form
"""

import random
import codecs

import pickle
import nltk
from nltk.tokenize import word_tokenize


def mad_libs(filename):
    """
    Replace random words in a file with other words
        with the same part of speech (aka mad libs)
    """
    start_text = choose_passage(filename)
    parts_of_speech = {'NN':' noun', 'NNS':' plural noun',
        'NNP':' proper noun', 'NNPS':' plural proper noun',
        'JJ':'n adjective', 'JJR':'n adjective', 'JJS':'n adjective',
        'RB':'n adverb', 'RBR':'n adverb', 'RBS':'n adverb',
        'VB':' verb', 'VBD':' verb', 'VBG':' verb', 'VBN':' verb',
        'VBP':' verb', 'VBZ':' verb'}

    mad_text = ''
    for word in start_text:
        if len(word[1]) > 1:
                mad_text += ' '
        if len(word[0]) > 3 \
            and word[1] in parts_of_speech \
            and random.randint(0, 6) == 0:
            mad_text += replace_word(word[0], parts_of_speech[word[1]])
        else:
            mad_text += word[0]
    return "\n\n Here is your lovely Mad-Lib: \n" + fix_formatting(mad_text)


def fix_formatting(text):
    stupid_things = ["''", "``", "\\ ", "\\'"]
    newtext = text
    for stupid in stupid_things:
        newtext = newtext.replace(stupid, '')  # delete these
    newtext = newtext.replace("\\r\\n", " ")  # replace with space
    return newtext


def replace_word(word, pos):
    """
    Takes a word and part of speech both as a strings
        outputs a user input word as a string
    """
    return raw_input('\nchoose a%s :\n' % pos)


def choose_passage(filename):
    """
    Takes a file and returns one paragraph split into
    a list of words tagged with their part of speech
    """
    f = open(filename, mode='r+')
    min_len = 500
    full = f.read()

    bookends = '\\r\\n' * 10
    book = full[full.find(bookends) + len(bookends) : full.rfind(bookends)]
    paragraphs = book.split('\\r\\n\\r\\n')
    par_opts = [i for i in paragraphs if len(i) > min_len]
    par = random.choice(par_opts)

    word_list = word_tokenize(par)
    return nltk.pos_tag(word_list)


def main():
    import sys
    if len(sys.argv) > 1:
        print mad_libs(sys.argv[1])
    else:
        print mad_libs("Original_Sherlock.txt")


if __name__ == '__main__':
    main()
