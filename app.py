from flask import Flask, render_template, request
import pickle
from similarity_core import load_embeddings, most_similar

rarity_boost = 5.0
randomness = 1.0

app = Flask(__name__)

with open('embeddings.pkl', 'rb') as file:
    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word  = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    similar_words = []
    similar_words_boosted = []

    if request.method == 'POST':
        lowercase_word = request.form['word'].lower()

        num_words_to_output = int(request.form.get('num_words', 10))
        rarity_boost = float(request.form.get('rarity_boost', 1.0))
        randomness = float(request.form.get('randomness', 0.0))

        if lowercase_word in lowercase_word_to_index:
            similar_words, similar_words_boosted = most_similar(lowercase_word, word_list, word_vectors, lowercase_word_to_index, rarity_boost=rarity_boost, randomness=randomness, num_words_to_output=num_words_to_output)
        else:
            similar_words = ["Word not found in embeddings."]

    return render_template('index.html', similar_words=similar_words, similar_words_boosted=similar_words_boosted)


if __name__ == '__main__':
    app.run(debug=True)