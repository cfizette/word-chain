
from WordChains import MarkovChain

chain = MarkovChain.unpickle('trumpSpeechesDeg2')
chain.generate_text(None, 100)
