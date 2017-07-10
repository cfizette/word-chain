
from WordChains import WordChain

chain = WordChain.unpickle('MarkovChains2.0/TrumpSpeechesDeg2')
chain.generate_text(None, 100, print_to_console=True)
