import numpy as np
from nltk.tokenize import word_tokenize
import numpy as np
import re
import pickle
import codecs
import sys
from WordChains import  WordNode, WordChain, LetterChain


# use if getting ascii error... i guess...
reload(sys)
sys.setdefaultencoding('utf8')


text_file = open('TextFiles/TrumpSpeeches.txt', 'r')
txt = text_file.read()
print txt

# Remove all new lines
txt = txt.replace('\n', ' ')

# Remove hyperlinks
#txt = re.sub(r'https\S+', '', txt, flags=re.MULTILINE)

# Remove Emojis
#txt = txt.encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')

#
chain = LetterChain()
chain.get_letters(txt, 1)
chain.generate_text(print_to_console=True)
#chain.pickle('ShakespeareDeg1')





