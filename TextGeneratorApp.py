
from WordChains import WordChainOld
from Tkinter import *
from ScrolledText import ScrolledText
import timeit


# Load the markov chains
print 'Loading RRMartin...'
start_time = timeit.default_timer()
RRMartinDeg1 = WordChainOld.unpickle('MarkovChains/RRMartinDeg1')
RRMartinDeg2 = WordChainOld.unpickle('MarkovChains/RRMartinDeg2')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Trump...'
start_time = timeit.default_timer()
TrumpDeg2 = WordChainOld.unpickle('MarkovChains/TrumpSpeechesDeg2')
TrumpDeg1 = WordChainOld.unpickle('MarkovChains/TrumpSpeechesDeg1')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Shakespeare...'
start_time = timeit.default_timer()
ShakespeareDeg2 = WordChainOld.unpickle('MarkovChains/ShakespeareDeg2')
ShakespeareDeg1 = WordChainOld.unpickle('MarkovChains/ShakespeareDeg1')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

print 'Loading Hillary...'
start_time = timeit.default_timer()
HillaryDeg2 = WordChainOld.unpickle('MarkovChains/HillarySpeechesDeg2')
HillaryDeg1 = WordChainOld.unpickle('MarkovChains/HillarySpeechesDeg1')
print 'Elapsed time: ', (timeit.default_timer() - start_time)

# Initialize tkinter stuff
root = Tk()
option = IntVar()
degree = IntVar()


def generate():
    print 'attempting to generate text'
    print option.get()
    if option.get() == 1:
        if degree.get() == 1:
            text.insert('1.0', RRMartinDeg1.generate_text(None, 100, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', RRMartinDeg2.generate_text(None, 100, continuous=True))
    elif option.get() == 2:
        if degree.get() == 1:
            text.insert('1.0', TrumpDeg1.generate_text(None, 100, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', TrumpDeg2.generate_text(None, 100, continuous=True))
    elif option.get() == 3:
        if degree.get() == 1:
            text.insert('1.0', HillaryDeg1.generate_text(None, 100, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', HillaryDeg2.generate_text(None, 100, continuous=True))
    elif option.get() == 4:
        if degree.get() == 1:
            text.insert('1.0', ShakespeareDeg1.generate_text(None, 100, continuous=True))
        elif degree.get() == 2:
            text.insert('1.0', ShakespeareDeg2.generate_text(None, 100, continuous=True))

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




