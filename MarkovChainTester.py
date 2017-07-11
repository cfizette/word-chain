
from WordChains import WordChain
import json

chain = WordChain.unpickle('MarkovChains2.0/TrumpSpeechesDeg2')
# #chain.generate_text(None, 100, print_to_console=True)
#
chain.to_csv('test.txt')

chain2 = WordChain()
chain2.from_csv('test.txt')
print chain2.dic.values()
chain2.generate_text(None, 100, print_to_console=True)

