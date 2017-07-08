import numpy as np
import pickle
import cPickle


class WordNode:

    def __init__(self, text):
        # store what the text is so it can be used later
        self.text = text
        self.followers = []  # followers used to keep track of probabilities
        self.dic = {}  # dic used to check if follower exists, faster than checking whole follower list
        self.word_count = []
        self.probabilities = []
        self.left = None
        self.right = None

    def update_probabilities(self):
        total_word_count = sum(self.word_count)
        # for I in range(0, len(self.followers)):  # for each word
        #     if I <= len(self.probabilities) - 1:  # for the old words
        #         self.probabilities[I] = float(self.word_count[I])/total_word_count
        #     else:  # for the new word
        #         self.probabilities.append(float(self.word_count[I]) / total_word_count)

        for I in range(0, len(self.followers)):  # for each word
            self.probabilities.append(float(self.word_count[I]) / total_word_count)

    def add_followers(self, word):
        if word not in self.dic:  # if this is a new word, add to list
            self.dic[word] = 1  # add key to dictionary, value doesn't matter
            self.followers.append(word)
            self.word_count.append(1)
        else:
            self.word_count[self.followers.index(word)] += 1  # increment word count

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


class LetterChain:

    def __init__(self):
        self.dic = {}
        self.capitals = []

    def pickle(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def unpickle(filename):
        with file(filename, 'rb') as f:
            return cPickle.load(f)

    # --------------------------------------
    # Extract Markov Chain from sample text
    # --------------------------------------
    def get_letters(self, TXT, degree):

        # TXT: String of text to analyze. May require prepossessing.
        # degree: Degree of Markov Chain to be created.

        TXT = list(TXT)
        frame = []  # contains object references for fast modifications
        dic = self.dic
        dic[' '.join(TXT[0:degree])] = WordNode(''.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            s = ''.join(TXT[i:degree + i])
            node = WordNode(s)
            dic[s] = node
            # frame.append(node)

            frame.append(s)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ''.join(TXT[i:i + degree])

            try:
                new_node = dic[s]  # see if current word has already been seen

            except KeyError:
                new_node = WordNode(s)
                dic[s] = new_node
                # Assume capital words are sentence starters
                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)

            frame.append(s)
            dic[frame[0]].add_followers(s)
            frame.pop(0)

        for key in dic:
            dic[key].update_probabilities()  # only needs to be done once at the end

        self.dic = dic

    # --------------------------------------
    # Generate text from Markov Chain
    # --------------------------------------
    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):

        # seed_array: A list of strings used to start sentences
        # num:        Number of iterations. Multiple sentences may be generated each iteration
        # continuous: If true then each iteration will take into account the ending of the previous iteration when
        #             beginning a new sentence

        generated = 0
        text = ''

        # If no seed is given, choose a starting phrase from the markov chain
        if seed_array is None:
            letters = self.dic[np.random.choice(self.capitals)]
        else:
            seed = np.random.choice(seed_array)
            letters = self.dic[seed]

        # Generate text
        while generated < num:
            sent = letters.text
            while True:
                string = letters.choose_next()  # choose next letters
                nextWord = self.dic[string]  # find the object corresponding to the chosen letters
                sent = sent + nextWord.text  # append new letters to text
                letters = nextWord
                if nextWord.text.endswith('.'):  # text ends when a sentence ends on a period
                    if print_to_console:
                        print sent
                    text = text + sent + '\n\n'  # Add to generated text and start a new line
                    break
            generated += 1

            if not continuous:  # new starting phrase chosen from list of all starting phrases
                if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
                    letters = self.dic[np.random.choice(self.capitals)]
                else:
                    seed = np.random.choice(seed_array)
                    letters = self.dic[seed]
            else:                # new starting phrase chosen from current node
                string = letters.choose_next()
                letters = self.dic[string]
        return text


class WordChain:

    def __init__(self):
        self.dic = {}
        self.capitals = []

    def pickle(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def unpickle(filename):
        with file(filename, 'rb') as f:
            return cPickle.load(f)

    # --------------------------------------
    # Extract Markov Chain from sample text
    # --------------------------------------
    def get_words(self, TXT, degree):
        # TXT: String of text to analyze. May require prepossessing.
        # degree: Degree of Markov Chain to be created. Unless corpus really really really large, don't use more than 2.

        TXT = TXT.split()
        frame = []
        dic = self.dic
        dic[' '.join(TXT[0:degree])] = WordNode(' '.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            s = ' '.join(TXT[i:degree+i])
            node = WordNode(s)
            dic[s] = node
            frame.append(s)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ' '.join(TXT[i:i + degree])

            try:
                new_node = dic[s]  # see if current word has already been seen

            except KeyError:
                new_node = WordNode(s)
                dic[s] = new_node
                # Assume capital words are sentence starters
                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)

            frame.append(s)
            dic[frame[0]].add_followers(s)
            frame.pop(0)

        for key in dic:
            dic[key].update_probabilities()  # only needs to be done once at the end

        self.dic = dic

    # --------------------------------------
    # Generate text from Markov Chain
    # --------------------------------------
    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):

        # seed_array: A list of strings used to start sentences
        # num:        Number of iterations. Multiple sentences may be generated each iteration
        # continuous: If true then each iteration will take into account the ending of the previous iteration when
        #             beginning a new sentence

        generated = 0
        text = ''

        # If no seed is given, choose a starting phrase from the markov chain
        if seed_array is None:
            word = self.dic[np.random.choice(self.capitals)]
        else:
            seed = np.random.choice(seed_array)
            word = self.dic[seed]

        # Generate text
        while generated < num:
            sent = word.text
            while True:
                string = word.choose_next()  # choose next word
                nextWord = self.dic[string]  # find the object corresponding to the chosen word
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
                    word = self.dic[np.random.choice(self.capitals)]
                else:
                    seed = np.random.choice(seed_array)
                    word = self.dic[seed]
            else:                # new starting phrase chosen from current node
                string = word.choose_next()
                word = self.dic[string]

        return text


# Kept for compatibility with TextGeneratorApp -----------------------------------------------
class WordNodeOld:

    def __init__(self, text):
        # store what the text is so it can be used later
        self.text = text
        self.followers = []  # followers used to keep track of probabilities
        self.dic = {}  # dic used to check if follower exists, faster than checking whole follower list
        self.word_count = []
        self.probabilities = []
        self.left = None
        self.right = None

    def update_probabilities(self):
        total_word_count = sum(self.word_count)
        # for I in range(0, len(self.followers)):  # for each word
        #     if I <= len(self.probabilities) - 1:  # for the old words
        #         self.probabilities[I] = float(self.word_count[I])/total_word_count
        #     else:  # for the new word
        #         self.probabilities.append(float(self.word_count[I]) / total_word_count)

        for I in range(0, len(self.followers)):  # for each word
            self.probabilities.append(float(self.word_count[I]) / total_word_count)

    def add_followers(self, word):
        if word not in self.dic:  # if this is a new word, add to list
            self.dic[word] = 1  # add key to dictionary, value doesn't matter
            self.followers.append(word)
            self.word_count.append(1)
        else:
            self.word_count[self.followers.index(word)] += 1  # increment word count

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


class WordChainOld:

    def get_capitals(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitals.append(w)

    def __init__(self, dic=None):
        self.dic = {}
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

        TXT = TXT.split()
        frame = []  # contains object references for fast modifications
        dic = self.dic
        dic[' '.join(TXT[0:degree])] = WordNodeOld(' '.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            s = ' '.join(TXT[i:degree+i])
            node = WordNodeOld(s)
            dic[s] = node
            #frame.append(node)

            frame.append(s)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ' '.join(TXT[i:i + degree])

            try:
                new_node = dic[s]  # see if current word has already been seen

            except KeyError:
                new_node = WordNodeOld(s)
                dic[s] = new_node
                # Assume capital words are sentence starters
                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)

            frame.append(s)
            dic[frame[0]].add_followers(s)
            frame.pop(0)

        for key in dic:
            dic[key].update_probabilities()  # only needs to be done once at the end

        self.dic = dic

    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):
        generated = 0
        text = ''  # Text to be returned

        if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
            word = self.dic[np.random.choice(self.capitals)]
        else:
            seed = np.random.choice(seed_array)  # seed_array is a list of strings
            word = self.dic[seed]  # find a node with that string associated with it

        while generated < num:
            sent = word.text

            while True:
                string = word.choose_next()  # choose next word
                nextWord = self.dic[string]  # find the object corresponding to the chosen word
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
                    word = self.dic[np.random.choice(self.capitals)]
                else:
                    seed = np.random.choice(seed_array)
                    word = self.dic[seed]
            else:                # new starting phrase chosen from current node
                string = word.choose_next()
                word = self.dic[string]

        return text


class LetterChainOld:

    # I don't think this is used anywhere......
    def get_capitals(self):
        for w in self.words:
            if w.text[0].isupper() and w.text[1].islower():
                self.capitals.append(w)

    def __init__(self, dic=None):
        self.dic = {}
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
        frame = []  # contains object references for fast modifications
        dic = self.dic
        dic[' '.join(TXT[0:degree])] = WordNodeOld(''.join(TXT[0:degree]))

        # Add the start of the sequence to get it going
        for i in range(0, degree):
            s = ''.join(TXT[i:degree + i])
            node = WordNodeOld(s)
            dic[s] = node
            # frame.append(node)

            frame.append(s)

        # Add the rest of the tokens
        for i in range(degree, len(TXT)):
            if i % 1000 == 0:
                print i
            s = ''.join(TXT[i:i + degree])

            try:
                new_node = dic[s]  # see if current word has already been seen

            except KeyError:
                new_node = WordNodeOld(s)
                dic[s] = new_node
                # Assume capital words are sentence starters
                if degree == 1:
                    if s[0].isupper():
                        self.capitals.append(s)

                elif s[0].isupper() and s[1].islower():
                    self.capitals.append(s)

            frame.append(s)
            dic[frame[0]].add_followers(s)
            frame.pop(0)

        for key in dic:
            dic[key].update_probabilities()  # only needs to be done once at the end

        self.dic = dic

    def generate_text(self, seed_array=None, num=50, continuous=True, print_to_console=False):

        # Copied code from WordChain. In this function "word" means "letters". I'm too lazy to fix this and no one will
        # probably ever see this anyways
        generated = 0
        text = ''  # Text to be returned
        if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
            word = self.dic[np.random.choice(self.capitals)]
        else:
            seed = np.random.choice(seed_array)  # seed_array is a list of strings
            word = self.dic[seed]  # find a node with that string associated with it

        while generated < num:
            sent = word.text

            while True:
                string = word.choose_next()  # choose next word
                nextWord = self.dic[string]  # find the object corresponding to the chosen word
                sent = sent + nextWord.text  # append new word to text
                word = nextWord
                if nextWord.text.endswith('.'):  # text ends when a sentence ends on a period
                    if print_to_console:
                        print sent
                    text = text + sent + '\n\n'  # Add to generated text and start a new line
                    break

            generated += 1

            if not continuous:  # new starting phrase chosen from list of all starting phrases
                if seed_array is None:  # if no seed is given, choose a starting phrase from the markov chain
                    word = self.dic[np.random.choice(self.capitals)]
                else:
                    seed = np.random.choice(seed_array)
                    word = self.dic[seed]
            else:                # new starting phrase chosen from current node
                string = word.choose_next()
                word = self.dic[string]
        return text









