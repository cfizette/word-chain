import numpy as np
from nltk.tokenize import word_tokenize
import numpy as np
import re
import pickle
import cPickle


class WordNode:

    def __init__(self, text):
        # store what the text is so it can be used later
        self.text = text
        self.followers = []
        self.word_count = []
        self.probabilities = []
        self.left = None
        self.right = None

    def update_probabilities(self):
        for I in range(0, len(self.followers)):  # for each word
            if I <= len(self.probabilities) - 1:  # for the old words
                self.probabilities[I] = float(self.word_count[I])/sum(self.word_count)
            else:  # for the new word
                self.probabilities.append(float(self.word_count[I]) / sum(self.word_count))

    def add_followers(self, word):
        #word = word.lower()
        if word not in self.followers:  # if this is a new word, add to list
            self.followers.append(word)
            self.word_count.append(1)
            self.update_probabilities()  # update probabilities
        else:
            self.word_count[self.followers.index(word)] += 1  # increment word count
            self.update_probabilities()  # update probabilities

    def choose_next(self):

        return np.random.choice(self.followers, p=self.probabilities)

    def add(self, node):
        # Do nothing if they are the same
        if node.text == self.text:
            return

        # Recursive methods for adding nodes to trees
        elif node.text < self.text:
            if self.left is None:
                self.left = node
            else:
                self.left.add(node)

        elif node.text > self.text:
            if self.right is None:
                self.right = node
            else:
                self.right.add(node)

    def find(self, txt):

        # If this is what is being searched for
        if txt == self.text:
            return self

        # Otherwise search left and right and return None if DNE
        if txt < self.text:
            if self.left is None:
                return None
            else:
                return self.left.find(txt)

        if txt > self.text:
            if self.right is None:
                return None
            else:
                return self.right.find(txt)


class WordChain:

    def get_capitals(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitals.append(w)

    def __init__(self, root=None):
        self.root = root
        self.capitals = []

    def pickle(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def unpickle(filename):
        with file(filename, 'rb') as f:
            return cPickle.load(f)

    def get_words(self, TXT, degree):

        TXT = word_tokenize(TXT)
        frame = []
        root = WordNode(' '.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            node = WordNode(' '.join(TXT[i:degree+i]))
            root.add(node)
            frame.append(node)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ' '.join(TXT[i:i + degree])
            old_instance = root.find(s)
            if old_instance is None:
                new_node = WordNode(s)
                root.add(new_node)
                # Assume capital words are sentence starters
                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)
            else:
                new_node = old_instance   # make sure the old object is the one getting changed
            frame.append(new_node)
            frame[0].add_followers(s)
            frame.pop(0)  # remove first element, frame is now back to original length
        self.root = root

    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):
        generated = 0
        text = ''  # Text to be returned

        if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
            word = self.root.find(np.random.choice(self.capitals))
        else:
            seed = np.random.choice(seed_array)  # seed_array is a list of strings
            word = self.root.find(seed)  # find a node with that string associated with it

        while generated < num:
            sent = word.text

            while True:
                string = word.choose_next()  # choose next word
                nextWord = self.root.find(string)  # find the object corresponding to the chosen word
                sent = sent + ' ' + nextWord.text  # append new word to text
                word = nextWord
                if nextWord.text.endswith('.'):  # text ends when a sentence ends on a period
                    if print_to_console:
                        print sent
                    text = text + sent + '\n\n'  # Add to generated text and start a new line
                    break

            generated += 1

            if not continuous:  # new starting phrase chosen from list of all starting phrases
                if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
                    word = self.root.find(np.random.choice(self.capitals))
                else:
                    seed = np.random.choice(seed_array)
                    word = self.root.find(seed)
            else:                # new starting phrase chosen from current node
                string = word.choose_next()
                word = self.root.find(string)

        return text


class LetterChain:

    # I don't think this is used anywhere......
    def get_capitals(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitals.append(w)

    def __init__(self, root=None):
        self.root = root
        self.capitals = []

    def pickle(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def unpickle(filename):
        with file(filename, 'rb') as f:
            return cPickle.load(f)

    def get_letters(self, TXT, degree):
        TXT = list(TXT)
        frame = []
        root = WordNode(''.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            node = WordNode(''.join(TXT[i:degree + i]))
            root.add(node)
            frame.append(node)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ''.join(TXT[i:i + degree])
            old_instance = root.find(s)
            if old_instance is None:
                new_node = WordNode(s)
                root.add(new_node)

                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)
            else:
                new_node = old_instance  # make sure the old object is the one getting changed
            frame.append(new_node)
            frame[0].add_followers(s)
            frame.pop(0)  # remove first element, frame is now back to original length
        self.root = root

    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):

        # Copied code from WordChain. In this function "word" means "letters". I'm too lazy to fix this and no one will
        # probably ever see this anyways
        generated = 0
        text = ''  # Text to be returned

        if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
            word = self.root.find(np.random.choice(self.capitals))
        else:
            seed = np.random.choice(seed_array)  # seed_array is a list of strings
            word = self.root.find(seed)  # find a node with that string associated with it

        while generated < num:
            sent = word.text

            while True:
                string = word.choose_next()  # choose next letters
                nextWord = self.root.find(string)  # find the object corresponding to the chosen letters
                sent = sent + nextWord.text  # append new letters to text
                word = nextWord
                if nextWord.text.endswith('.'):  # text ends when a sentence ends on a period
                    if print_to_console:
                        print sent
                    text = text + sent + '\n\n'  # Add to generated text and start a new line
                    break

            generated += 1

            if not continuous:  # new starting phrase chosen from list of all starting phrases
                if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
                    word = self.root.find(np.random.choice(self.capitals))
                else:
                    seed = np.random.choice(seed_array)
                    word = self.root.find(seed)
            else:                # new starting phrase chosen from current node
                string = word.choose_next()
                word = self.root.find(string)

        return text















