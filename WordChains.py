import numpy as np
from nltk.tokenize import word_tokenize
import numpy as np
import re
import pickle
import cPickle


class Word:
    #use np.random.choice to choose following word

    def __init__(self, text):
        # store what the text is so it can be used later
        self.text = text
        self.followers = []
        self.word_count = []
        self.probabilities = []

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

    def choose_new_word(self):
        return np.random.choice(self.followers, p=self.probabilities)


class Chain:

    capitalWords = []

    def get_capital_words(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitalWords.append(w)

    def __init__(self, words):
        self.words = words
        # Get capital words for later use
        self.get_capital_words()


    def pickle(self, filename):
        f = file(filename, 'wb')
        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def unpickle(filename):
        with file(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def get_words(TXT, degree):
        TXT = word_tokenize(TXT)
        #TXT = re.split()
        word_markchain = []
        # word_markchain.append(Word(' '.join(TXT[0:degree])))
        # word_markchain.append(Word(' '.join(TXT[1:degree+1])))
        for i in range(0, degree):
            word_markchain.append(Word(' '.join(TXT[i:degree+i])))
        #print ' '.join(TXT[0:degree])
        for i in range(degree, len(TXT)):
            print i
            s_prev = ' '.join(TXT[i-degree:i])
            print s_prev
            s = ' '.join(TXT[i:i+degree])


            # Add this word to the previous words followers
            # print next((w for w in wordChain if w.text == s_prev)).followers
            next((w for w in word_markchain if w.text == s_prev)).add_followers(s)

            # if the word has not been seen before
            if not any(w.text == s for w in word_markchain):
                word_markchain.append(Word(s))

        return word_markchain

    def generate_text(self, seed_array, num):
        generated = 0
        print self.capitalWords
        while generated < num:

            if seed_array == None:  # if no seed is given, choose a starting phrase from the markov chain
                word = np.random.choice(self.capitalWords)
            else:
                seed = np.random.choice(seed_array)
                word = next((w for w in self.words if w.text.startswith(seed)))

            sent = word.text

            while True:
                string = word.choose_new_word()

                nextWord = next((w for w in self.words if w.text == string))
                sent = sent + ' ' + nextWord.text

                if nextWord.text.endswith('.'):
                    print sent
                    break
                word = nextWord

            generated += 1


class WordNode:
    #use np.random.choice to choose following word

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

    def choose_new_word(self):

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


class BinaryChain:

    def get_capital_words(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitalWords.append(w)

    def __init__(self, root=None):
        self.root = root
        self.capitalWords = []
        # Get capital words for later use
        #self.get_capital_words()

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
            # New Method----
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
                # print s[0]
                # print s[1]
                if degree == 1:
                    if s[0].isupper():
                        self.capitalWords.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitalWords.append(s)
            else:
                new_node = old_instance   # attempt to make sure the old object is the one getting changed
            frame.append(new_node)
            frame[0].add_followers(s)
            frame.pop(0)  # remove first element
        self.root = root

    def generate_text(self, seed_array, num, continuous=True, print_to_console=False):
        generated = 0
        text = ''  # Text to be returned
        print self.capitalWords

        if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
            word = self.root.find(np.random.choice(self.capitalWords))
        else:
            seed = np.random.choice(seed_array)  # seed_array is a list of strings
            word = self.root.find(seed)  # find a node with that string associated with it


        while generated < num:

            sent = word.text

            while True:
                string = word.choose_new_word()

                nextWord = self.root.find(string)

                sent = sent + ' ' + nextWord.text

                word = nextWord

                if nextWord.text.endswith('.'):
                    if print_to_console:
                        print sent
                    text = text + sent + '\n\n'  # Add to generated text and start a new line
                    break

            generated += 1

            if not continuous:
                if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
                    word = self.root.find(np.random.choice(self.capitalWords))
                else:
                    seed = np.random.choice(seed_array)
                    word = self.root.find(seed)
            else:  # We want continous sentences... needs work... i think i fixed it
                string = word.choose_new_word()
                word = self.root.find(string)

        return text


















