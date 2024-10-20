from similarity_core import load_embeddings
import pickle

def main():
    num_words_to_load = None

    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings(num_words_to_load)

    with open('embeddings.pkl', 'wb') as f:
        pickle.dump((word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word), f)

    print(f"Loaded {len(word_list)} words from embeddings and saved to embeddings.pkl.")

if __name__ == "__main__":
    main()

