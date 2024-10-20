# DictionWave 

DictionWave is a word-discovery tool that lets you surf across the world of English language and meaning, using the power of word embeddings. It uses word vector similarities, a rarity parameter, and some randomness, to facilitate word discovery.

Please see the demonstration video below for an example of what DictionWave can do.

https://private-user-images.githubusercontent.com/11036537/378196693-793a063b-b767-4621-bd6f-06c004b7c604.mp4

Alternatively, here is some terminal output from the main implementation file `similarity_core.py`, with a 100,000 word vocabulary, 50 words per query, a "rarity boost" factor of 5, and a randomness factor of 0. 

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

I hope you enjoy exploring the English language with DictionWave! For implementation details, please see [`similarity_core.py`](./similarity_core.py). If you want to set it up for yourself, please see the instructions below. I plan on making the web application shown in the video above publicly accessible as soon as I can.

## Development Setup

1. Open your terminal and clone this repostory:
    ```
    git clone https://github.com/jhelsby/DictionWave.git 
    cd DictionWave
    ```

    Install the required packages:
    ```
    pip install -r requirements.txt
    ```

2. Download a file of word vectors, where each line is of the format `[word] [vector]` (e.g. `use -0.1545 0.0836  [...] 0.1351`), and place it at the repository root. 

    * I used `crawl-300d-2M.vec`, a freely available collection of 2 million word vectors trained on [Common Crawl](https://en.wikipedia.org/wiki/Common_Crawl). You can download the model [here](https://fasttext.cc/docs/en/english-vectors.html).

3. (Optional.) Create a `blacklist.txt` file to filter out words from your data source. Since `crawl-300d-2M.vec` is raw research data collected from the web, there are a number of explicit and derogatory words included in the word vectors which you may not wish to appear when running DictionWave.

    *  I manually assembled my own blacklist file, but since it is primarily a list of slurs and obscenities I did not wish to host it in this repository. If you would like to use it, please contact me.

4. Run `python filter_embeddings.py`. First, this filters out duplicates, redundant words, and any blacklisted words from your dataset. Then, it saves the embeddings to a `embeddings.pkl` file for later use. You may need to change the `input_file` variable name to match your word vectors filename.

    * My combination of filters reduced the 2 million word source file to 1,240,641 words at the last count. I am going to continuing trying to bring this number down, as there is a still lot of redundancy in there, such as misspellings. A cleaner dataset will let DictionWave run faster and return better results.
    
    * (Optional) If you run this script yourself, you may wish to set `total_number_of_words` in `similarity_core.py` to be equal to the number of words `filter_embeddings.py` tells you are left in the input, so the loading bars are configured correctly. Precomputing this number saves time when loading the embeddings later on.

5. To run the program in your terminal, run `python similarity_core.py` and follow the instructions it provides. To run the program as a Flask web application, run `python app.py`.

## References

I used [fastText](https://fasttext.cc/), the provider of `crawl-300d-2M.vec`, to create DictionWave. As per the request of the fastText project, I would therefore like to cite the following paper:

T. Mikolov, E. Grave, P. Bojanowski, C. Puhrsch, A. Joulin. [Advances in Pre-Training Distributed Word Representations](https://arxiv.org/abs/1712.09405).