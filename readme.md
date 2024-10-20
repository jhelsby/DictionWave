# DictionWave 

DictionWave is a word-discovery tool that lets you surf across  the world of English language and meaning. Here's how to use it:

1. Download a word vectors file and set it up in the repository.

2. Run DictionWave, and select:
    * the size of the vocabulary you wish to load from the vectors file.
    * how many words you would like to be shown for each input.
    * a "rarity boost" factor - this will determine how common or rare the words you are shown will be.
    * a "randomness" factor - to mix up the exploration some more, and show you words you might not have seen before.

3. Enter whichever words you are curious to dive into further. 

I hope you enjoy exploring the English language with DictionWave! Here's an example of what it can do, with a 100,000 word vocabulary, 50 words per query, a rarity boost factor of 5, and a randomness factor of 0. 

```
> Enter a word: Shakespeare

Most similar words:

Coriolanus Jacobean Romeo Wordsworth Sophocles 
sonnets Mercutio Oedipus Marlowe Macbeth dramatist 
Pygmalion Hamlet Shrew Shakespearian Jonson
Stratford-upon-Avon playwriting soliloquy playwrights
Bard Brecht Shylock Pericles Lear Juliet Dickens
sonnet Chekhov dramatists Falstaff Iago Aeschylus
Polonius Elizabethan Yeats Euripides Othello
Shakespearean Moliere Antigone Chaucer playwright
Keats Stratford Goethe Ibsen Branagh Ophelia Folger

Rarity boosted words:

Mercutio Capulet playhouses Aeschylus Spamalot
Faustus Covent Godspell Pericles Benedick Ibsen
Shakespearean Catullus Aeneid Brontë stagecraft
Sophocles Tybalt Aristophanes Caxton Mamet
Stratford-upon-Avon Euripides Petrarch Lucretius 
Monteverdi dramatists Pepys Jonson Bankside Folger
playwriting Moliere Jacobean Otello Boethius 
Shakespearian Branagh Laertes Blackfriars
Polonius Coriolanus Rosaline Hazlitt Albee
Metamorphoses Pygmalion Moby-Dick Malory Banquo
```

Please see below for more detailed instructions on how to set up this project. I also plan to deploy DictionWave as a self-contained web application in the near future.

## Setup

1. Open your terminal and clone this repostory:
    ```
    git clone https://github.com/jhelsby/DictionWave.git 
    cd DictionWave
    ```

    Install the packages listed in `requirements.txt`.

2. Download a file of word vectors, and place it at the repository root. I used `crawl-300d-2M.vec`, a freely available collection of 2 million word vectors trained on [Common Crawl](https://en.wikipedia.org/wiki/Common_Crawl). You can download the model [here](https://fasttext.cc/docs/en/english-vectors.html).

3. (Optional.) Create a `blacklist.txt` file to filter out words from your data source. Since `crawl-300d-2M.vec` is raw research data collected from the web, there are a number of explicit and derogatory words included in the word vectors which you may not wish to appear when running DictionWave.

    I manually assembled my own blacklist file, but since it is primarily a list of slurs and obscenities I did not wish to host it in this repository. If you would like to use it, please contact me.

4. Run `python filter_embeddings.py` to filter out duplicates, redundant words, and any blacklisted words from your dataset. You may need to change the `input_file` variable name to match your word vectors filename.

5. Run `python main.py` and follow the instructions it provides.

## References

I used [fastText](https://fasttext.cc/), the providers of `crawl-300d-2M.vec`, to create DictionWave. As per the request of the fastText project, I would therefore like to cite the following paper:

T. Mikolov, E. Grave, P. Bojanowski, C. Puhrsch, A. Joulin. [Advances in Pre-Training Distributed Word Representations](https://arxiv.org/abs/1712.09405).