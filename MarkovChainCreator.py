import numpy as np
from nltk.tokenize import word_tokenize
import numpy as np
import re
import pickle
import codecs
import sys
from WordChains import Word, WordNode, Chain, BinaryChain


# use if getting ascii error... i guess...
reload(sys)
sys.setdefaultencoding('utf8')


text_file = open('Shakespeare.txt', 'r')
txt = text_file.read()
print txt

# Remove all new lines
txt = txt.replace('\n', ' ')

# Remove hyperlinks
#txt = re.sub(r'https\S+', '', txt, flags=re.MULTILINE)

# Remove Emojis
#txt = txt.encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')

#
chain = BinaryChain()
chain.get_words(txt, 1)
chain.pickle('ShakespeareDeg1')





