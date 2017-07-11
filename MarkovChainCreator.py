
import timeit
import sys
from WordChains import  WordNode, WordChain, LetterChain, WordChainOld


# use if getting ascii error... i guess...
reload(sys)
#sys.setdefaultencoding('utf8')


text_file = open('TextFiles/CompleteRRMartin.txt', 'r')
txt = text_file.read()
print txt

# Remove all new lines
txt = txt.replace('\n', ' ')

# Remove hyperlinks
#txt = re.sub(r'https\S+', '', txt, flags=re.MULTILINE)

# Remove Emojis
#txt = txt.encode("utf-8").decode('unicode_escape').encode('ascii', 'ignore')

#
chain = WordChain()
start_time = timeit.default_timer()
chain.get_words(txt, 1)
time = (timeit.default_timer() - start_time)
chain.generate_text(print_to_console=True)
print 'Elapsed time: ', time
# for key, words in chain.dic.items():
#     print words.followers
chain.to_csv('MarkovChains2.0/CompleteRRMartinDeg1.txt')





