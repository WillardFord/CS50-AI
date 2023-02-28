import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Det N | Det Adj NP | Adj NP 
VP -> V | VP PP | Adv VP | VP NP | VP Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    lowered = sentence.lower()
    word_list = nltk.word_tokenize(lowered)
    # Remove non alpha words
    for word in word_list:
        valid = False
        for letter in word:
            if letter.isalpha():
                valid = True
                break
        if not valid:
            word_list.remove(word)
    return word_list

def containsNP(tree):
    if tree.label() == "NP": return True
    if len(tree) == 1 and tree.label() != 'S':
        return False 
    for subtree in tree:
        if containsNP(subtree):
            return True
    return False

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    output = []

    for subtree in tree:
        hasNP = containsNP(subtree)
        if not hasNP: continue
        if subtree.label() in ["S","NP","VP","PP"]:
            output += np_chunk(subtree)

    if tree.label() == "NP" and not hasNP: 
        output.append(tree)
    return output



if __name__ == "__main__":
    main()
