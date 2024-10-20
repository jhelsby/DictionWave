from flask import Flask, render_template, request
import os, pickle, random
import dotenv
import gdown
from threading import Thread
from similarity_core import most_similar

rarity_boost = 5.0
randomness = 1.0
lite_embeddings_filepath = 'embeddings_lite.pkl'

app = Flask(__name__)

dotenv.load_dotenv()

def load_embeddings_from_file(embeddings_filepath):
    with open(embeddings_filepath, 'rb') as file:
        word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word  = pickle.load(file)

        return word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word

def load_full_embeddings():
    full_embeddings_filepath = 'embeddings.pkl'
    if not os.path.exists(full_embeddings_filepath):
        gdrive_file_id = os.getenv('GDRIVE_EMBEDDINGS_FILE_ID')
        gdown.download(f'https://drive.google.com/uc?id={gdrive_file_id}', full_embeddings_filepath, quiet=False)
        print("Full embeddings file downloaded.")
        global word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word
        word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings_from_file(full_embeddings_filepath)

def load_full_embeddings_in_background():
    thread = Thread(target=load_full_embeddings)
    thread.start()

word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings_from_file(lite_embeddings_filepath)

# If the server has over 2GB RAM, consider using the full embeddings set.
# load_full_embeddings_in_background()

@app.route('/', methods=['GET', 'POST'])
def index():
    similar_words = []
    similar_words_boosted = []
    word = None
    example_words = None

    if request.method == 'POST':
        word = request.form['word']
        lowercase_word = word.lower()

        num_words_to_output = int(request.form.get('num_words', 80))
        rarity_boost = float(request.form.get('rarity_boost', 5.0))
        randomness = float(request.form.get('randomness', 0.0))

        if lowercase_word in lowercase_word_to_index:
            similar_words, similar_words_boosted = most_similar(lowercase_word, word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word, rarity_boost=rarity_boost, randomness=randomness, num_words_to_output=num_words_to_output)
        else:
            similar_words = ["Word not found in embeddings."]
    
    else: 
        example_words = random.sample(list(word_list), min(len(word_list), 10))

    return render_template('index.html', similar_words=similar_words, similar_words_boosted=similar_words_boosted, last_word=word,example_words=example_words)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))