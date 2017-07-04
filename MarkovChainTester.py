
from WordChains import WordChain

chain = WordChain.unpickle('trumpSpeechesDeg2')
chain.generate_text(None, 100)
