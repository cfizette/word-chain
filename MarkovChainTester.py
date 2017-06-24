
from WordChains import BinaryChain

chain = BinaryChain.unpickle('trumpSpeechesDeg2')
chain.generate_text(None, 100)
