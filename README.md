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
```
# saving a WordChain object at location
chain.pickle(location) # using pickle
chain.to_csv(location) # saving as txt file
```
```
# loading a WordChain object
chain.unpickle(location) # using pickle
chain.from_csv(location) # loading from txt file
```

#### Markov Chain Creator
Script for creating a Markov chain from text files

#### Markov Chain Tester
Script for testing the text generated from a Markov chain created using the Markoc Chain Creator

#### Text Generator App
Sample application to show the results of text generation using Markov chains. Includes generators for Donald Trump, Hillary Clinton, Shakespeare, and George R.R. Martin. Can also choose between 1st order and 2nd order Markov chains for Trump, Clinton, and Shakespeare.

## More on how to use word-chain
- Text files should be converted into a single line string before passing into get_words() or get_letters().
- You may need to mess with the encoding of the input text or remove weird things like emojiis. Feel free to find a way around this though.
- Large corpuses are required in order to generate unique text. The size required increases as the author's text becomes more varied and as you increase the Markov Chain degree. The Trump text file included contains around 170,000 words and I find that 2nd degree markov chains prodced with it generate unique text (in other words, googling the output yields no results). However the Shakespeare file only contains around 20,000 words. Text generated using this file usually consists of whole sentences taken from different works.
- The "csv" files you can create consists of two main parts. The first line consists of a Markov Chain's "starters". For now capitalWords=starters. The rest of the file consists of three columns separated by | _ |. The columns contain
    1. A string
    2. A list of that string's "followers" 
    3. A list of probabilities corresponding to the "followers"
    
    The elements in the list of "followers" and probabilities are separated by |

## Possible FAQs
#### How long does it take to create a Markov Chain?
- Not that long. Creating a Markov Chain from the ~2mil word RRMartin example takes around 13 seconds. Generating one from the ~170,000 word TrumpSpeeches.txt file takes just under 1s. I will also keep looking for ways to increase efficiency.
#### Are there advantages or disadvantages between the different ways of saving a WordChain object?
- The .txt files are smaller than their corresponding pickle files. I will post more when I can better quantify this difference as well as attest to any differences in loading or saving speed. My initial reason for creating the .txt file method was to allow for the possibility of loading Markov Chains generating using word-chain into other programming languages.

## Things that need work
- [x] Formatting
- [x] Speed
- [ ] Larger Datasets
- [ ] Add saving to text file to LetterChain
