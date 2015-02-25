import pickle
from pattern.web import *

Sherlock_text = URL('http://www.gutenberg.org/cache/epub/1661/pg1661.txt'
					).download()

Sherlock = open('Original_Sherlock.txt', 'w')
pickle.dump(Sherlock_text, Sherlock)
Sherlock.close