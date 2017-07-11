# word-chain
A Python tool for generating text using Markov chains

## Files

#### WordChain.py
Contains Python classes for analyzing text files and generating text

Examples of functions:
```
# creating a markov chain of words of degree d from string txt
chain = WordChain()
chain.get_words(txt, d)
```
```
# generating text from a WordChain object
chain.generate_text()
```

#### Markov Chain Creator
Script for creating a Markov chain from text files

#### Markov Chain Tester
Script for testing the text generated from a Markov chain created using the Markoc Chain Creator

#### Text Generator App
Sample application to show the results of text generation using Markov chains. Includes generators for Donald Trump, Hillary Clinton, Shakespeare, and George R.R. Martin. Can also choose between 1st order and 2nd order Markov chains for Trump, Clinton, and Shakespeare.

## Things that need work
- [x] Formatting
- [x] Speed
- [ ] Larger Datasets
- [ ] Add saving to text file to LetterChain
