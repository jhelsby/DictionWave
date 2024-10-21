""""""

from similarity_core import load_embeddings
import pickle

# Choose whether to save all word embeddings, or 
# a <100MB subset of 74,000 words.
save_embeddings_lite_file = False
embeddings_lite_size = 74000

embeddings_lite_filename = 'embeddings_lite.pkl'
embeddings_full_filename = 'embeddings.pkl'

def main():
    # None loads all words.
    num_words_to_load = embeddings_lite_size if save_embeddings_lite_file else None
    output_filename = embeddings_lite_filename if save_embeddings_lite_file else embeddings_full_filename

    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings(num_words_to_load)

    with open(output_filename, 'wb') as f:
        pickle.dump((word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word), f)

    print(f"Loaded {len(word_list)} words from embeddings and saved to {output_filename}.")

if __name__ == "__main__":
    main()

