from similarity_core import load_embeddings
import pickle

is_embeddings_lite = False

def main():
    # None loads all words.
    # embeddings_lite has 74000 words - just under 100MB.

    num_words_to_load = 74000 if is_embeddings_lite else None

    output_filename = 'embeddings_lite.pkl' if is_embeddings_lite else 'embeddings.pkl'

    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings(num_words_to_load)

    with open(output_filename, 'wb') as f:
        pickle.dump((word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word), f)

    print(f"Loaded {len(word_list)} words from embeddings and saved to {output_filename}.")

if __name__ == "__main__":
    main()

