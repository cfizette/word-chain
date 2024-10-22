
from WordChains import WordChainOld, WordChain
from Tkinter import *
from ScrolledText import ScrolledText
import timeit

# Initialize tkinter stuff
root = Tk()
option = IntVar()
degree = IntVar()


# Load the markov chains
print 'Loading RRMartin...'
start_time = timeit.default_timer()
RRMartinDeg1 = WordChainOld.unpickle('MarkovChainsLegacy/CompleteRRMartinDeg1_L')
RRMartinDeg2 = WordChainOld.unpickle('MarkovChainsLegacy/CompleteRRMartinDeg2_L')
# RRMartinDeg1 = WordChain().from_csv('MarkovChains2.0/CompleteRRMartinDeg1.txt')
# RRMartinDeg2 = WordChain().from_csv('MarkovChains2.0/CompleteRRMartinDeg2.txt')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Trump...'
start_time = timeit.default_timer()
TrumpDeg2 = WordChainOld.unpickle('MarkovChainsLegacy/TrumpSpeechesDeg2_L')
TrumpDeg1 = WordChainOld.unpickle('MarkovChainsLegacy/TrumpSpeechesDeg1_L')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Shakespeare...'
start_time = timeit.default_timer()
ShakespeareDeg2 = WordChainOld.unpickle('MarkovChainsLegacy/ShakespeareDeg2_L')
ShakespeareDeg1 = WordChainOld.unpickle('MarkovChainsLegacy/ShakespeareDeg1_L')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Hillary...'
start_time = timeit.default_timer()
HillaryDeg2 = WordChainOld.unpickle('MarkovChainsLegacy/HillarySpeechesDeg2_L')
HillaryDeg1 = WordChainOld.unpickle('MarkovChainsLegacy/HillarySpeechesDeg1_L')
print 'Elapsed time: ', (timeit.default_timer() - start_time)


def generate():
    print 'attempting to generate text'
    print option.get()
    if option.get() == 1:
        if degree.get() == 1:
            text.insert('1.0', RRMartinDeg1.generate_text(None, 5, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', RRMartinDeg2.generate_text(None, 5, continuous=True))
    elif option.get() == 2:
        if degree.get() == 1:
            text.insert('1.0', TrumpDeg1.generate_text(None, 5, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', TrumpDeg2.generate_text(None, 5, continuous=True))
    elif option.get() == 3:
        if degree.get() == 1:
            text.insert('1.0', HillaryDeg1.generate_text(None, 5, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', HillaryDeg2.generate_text(None, 5, continuous=True))
    elif option.get() == 4:
        if degree.get() == 1:
            text.insert('1.0', ShakespeareDeg1.generate_text(None, 5, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', ShakespeareDeg2.generate_text(None, 5, continuous=True))

# Create Gui---------------------------------------------
# create and pack frames
button_frame = Frame(root)
bottom = Frame(root)
option_frame = Frame(button_frame)
degree_frame = Frame(button_frame)
button_frame.pack()
degree_frame.pack(side=RIGHT)
option_frame.pack()
bottom.pack(side=BOTTOM)

# create and pack elements
text = ScrolledText(bottom, undo=True, wrap=WORD)
# RadioButtons for choosing text
Radiobutton(option_frame, text="RRMartin", variable=option, value=1).pack(side=RIGHT)
Radiobutton(option_frame, text="Trump", variable=option, value=2).pack(side=RIGHT)
Radiobutton(option_frame, text="Hillary", variable=option, value=3).pack(side=RIGHT)
Radiobutton(option_frame, text="Shakespeare", variable=option, value=4).pack(side=RIGHT)

# Radiobuttons for choosing degree of markov chain
Radiobutton(degree_frame, text="Deg 1", variable=degree, value=1).pack()
Radiobutton(degree_frame, text="Deg 2", variable=degree, value=2).pack()

# Button for generating text
button = Button(button_frame, text='Generate Speech', command=generate)
button.pack()

text.pack(expand=True, fill='both')

root.mainloop()




