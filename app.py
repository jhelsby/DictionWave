"""
Flask web application logic for DictionWave.
"""

from flask import Flask, render_template, request, redirect, url_for
import os, pickle, random, requests
import dotenv
import gdown
from threading import Thread
from similarity_core import most_similar

rarity_boost = 5.0
randomness = 1.0
lite_embeddings_filepath = 'embeddings_lite.pkl'
full_embeddings_filepath = 'embeddings.pkl'

# Set whether to use the locally hosted, 74,000 word lite_embeddings file,
# or the full 1.2 million word embeddings file (which may need to be downloaded).
use_full_embeddings = False


app = Flask(__name__)

dotenv.load_dotenv()

def load_embeddings_from_file(embeddings_filepath):
    with open(embeddings_filepath, 'rb') as file:
        word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word  = pickle.load(file)

        return word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word

def load_full_embeddings():
    # If full_embeddings file doesn't exist, download it from Google Drive.
    if not os.path.exists(full_embeddings_filepath):
        gdrive_file_id = os.getenv('GDRIVE_EMBEDDINGS_FILE_ID')
        gdown.download(f'https://drive.google.com/uc?id={gdrive_file_id}', full_embeddings_filepath, quiet=False)
        print("Full embeddings file downloaded.")

    # Load full embeddings.
    global word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word
    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings_from_file(full_embeddings_filepath)

def load_full_embeddings_in_background():
    thread = Thread(target=load_full_embeddings)
    thread.start()

word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings_from_file(lite_embeddings_filepath)

# If the server has over 2GB RAM, consider using the full embeddings set.
if use_full_embeddings:
    load_full_embeddings_in_background()

@app.route('/', methods=['GET', 'POST'])
def index():
    similar_words = []
    similar_words_boosted = []
    word = None
    example_words = None

    if request.method == 'POST':
        word = request.form['word'].strip()
        lowercase_word = word.lower()

        num_words_to_output = int(request.form.get('num_words', 80))
        rarity_boost = float(request.form.get('rarity_boost', 5.0))
        randomness = float(request.form.get('randomness', 0.0))

        if lowercase_word in lowercase_word_to_index:
            similar_words, similar_words_boosted = most_similar(lowercase_word, word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word, rarity_boost=rarity_boost, randomness=randomness, num_words_to_output=num_words_to_output)
        else:
            similar_words = ["Word not found."]
    
    else: 
        example_lowercase_words = random.sample(list(word_list), min(len(word_list), 15))
        example_words = [lowercase_word_to_word[lowercase_word] for lowercase_word in example_lowercase_words]

    return render_template('index.html', similar_words=similar_words, similar_words_boosted=similar_words_boosted, last_word=word,example_words=example_words)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        response = requests.post(url_for('index', _external=True), data=request.form)

        return response.content  
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

