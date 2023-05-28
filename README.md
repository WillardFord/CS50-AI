# CS50-AI
I completed the [CS50 with AI](https://cs50.harvard.edu/ai/2020/) course by Harvard from January to March of 2023. It consisted of 2 projects completed each week summarised below:

## [Week 0:](https://cs50.harvard.edu/ai/2020/projects/0/)
### Degrees:
<p>The 7 degrees of Kevin Bacon. I implmented depth first seach on a datset pulled from the IBM api to determine how many far apart any two actors are. Actors who starred in a film together have a distance of 0.</p>

### Tic-Tac-Toe:
<p>I implemented mini-max in tic-tac-toe. An inefficient algorithm that solves the game it plays can only be viable for such a small game (especially on my computer).</p>

## [Week 1:](https://cs50.harvard.edu/ai/2020/projects/1/)
### Knights:
<p>This project was an excercise in propositional logic. Given a set of starting conditions can I algorithmically deduce the role (truth-value) of each knight or knave.</p>

### Minesweeper:
<p>I built an algorithm to solve Minesweeper. If there is a safe square available my AI will find it through its internal sets of safe squares and unsafe squares updated after each move. If there is no safe square known, it will heuristically make a decent guess.</p>

## [Week 2:](https://cs50.harvard.edu/ai/2020/projects/2/)
### PageRank:
<p>I implemented two models to rank a set of pages with links to each other by a set of probabilities. Firstly I used the random surfer, Markov model to travel between pages n times, storing the number of occurrences of each page. Secondly I used the links to develop a recursive summation equation the approximates the same thing. Then iteratively called it until the values stabilized. (Previously I have implemented a matrix to the n-th power solution)</p>

### Heredity:
<p>Given a set of parental genotypes of a somatic gene and probabilites of showing the disease phenotype for each genotype and any phenotypic information available about the offspring, I implemented a Baysean network to determine the probabilities of each phenotype in their offspring.</p>

## [Week 3:](https://cs50.harvard.edu/ai/2020/projects/3/)
### Crossword:
<p>I represent a crossword as a graph structure where the nodes represent words and the edges represent overlapping letters. This allowed me to implement the AC-3 algorithm and recursively backtrack to find a valid arrangement of words. Heuristics make a big difference in run time efficiency in this problem and as such significant time was spent to optimize this problem.</p>

## [Week 4:](https://cs50.harvard.edu/ai/2020/projects/4/)
### Shopping:
<p>I built a k-Nearest Neighbor classification system to determine whether or not a given shopper on a website was going to make a purchase using tidy data related to the shoppers activity on the website.</p>

### Nim:
<p>I implemented Q-learning to play the children's game of Nim. After letting the model play 10,000 games against itself, I was unable to beat it.</p>

## [Week 5:](https://cs50.harvard.edu/ai/2020/projects/5/)
### Traffic:
<p>Using a convolutional neural network in Tensorflow, I achieved 98% accuracy on identifying road signs in a dataset of 42 different road sigs. Finding a middle ground between accuracy and model complexity (and therefore training time) led me to use 2 convolutional layers and 2 fully connected layers. This compromise trains very quickly on my laptop and still achieves an impressive accruacy rate. To avoid overfitting I also experimented with a drop out rate but I found using a lower percentage of my data to train lead to faster training and also prevented overfitting.</p>

## [Week 6:](https://cs50.harvard.edu/ai/2020/projects/6/)
### Parser:
<p>I built a set of language rules and used them with nltk to build trees representing the grammar structure of any english sentence (using language from the limited lexicon). To implement more sentences, we would simply need to add more words and their grammatical type. These projects were the earliest version of Natural Language Processing before word2vec or generative AI blew up.</p>

### Questions:
<p>Given an input question, this algorithm returns the most relevant sentence from the corpus of documents available. By first ranking each document using the tf-idf algorithm and then ranking each sentence using a similar algorithm, each question can be reasonably assigned to a sentence that is mostly likely to answer their question. But there is no generative aspect in this model, therefore if the question is not answered by a sentence in the corpus then this model is unlikely to produce a satisfying answer.</p>
