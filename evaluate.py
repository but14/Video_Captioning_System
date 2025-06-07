import os
import numpy as np
import json
import joblib
from keras.models import load_model
from keras.layers import Input
from keras.models import Model
from keras.layers import LSTM, Dense
from keras.preprocessing.sequence import pad_sequences
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import config  # Import config từ file config.py


def load_test_data(test_path, tokenizer, max_length):
    test_label_path = os.path.join(test_path, 'testing_label.json')
    with open(test_label_path) as data_file:
        test_data = json.load(data_file)

    test_feat_path = os.path.join(test_path, 'feat')
    features = {}
    captions = {}

    for item in test_data:
        video_id = item['id']
        caps = ["<bos> " + c + " <eos>" for c in item['caption']]
        captions[video_id] = caps
        feature_file = os.path.join(test_feat_path, f"{video_id}.npy")
        features[video_id] = np.load(feature_file, allow_pickle=True)

    return features, captions


def build_inference_decoder(latent_dim, num_decoder_tokens):
    decoder_inputs = Input(shape=(1, num_decoder_tokens), name="decoder_inputs")
    decoder_state_input_h = Input(shape=(latent_dim,))
    decoder_state_input_c = Input(shape=(latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True, name='decoder_lstm')
    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_inputs, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]

    decoder_dense = Dense(num_decoder_tokens, activation='relu', name='decoder_relu')
    decoder_outputs = decoder_dense(decoder_outputs)

    decoder_model = Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return decoder_model, decoder_lstm, decoder_dense


def decode_sequence(encoder_model, decoder_model, input_seq, tokenizer, max_length, num_decoder_tokens):
    index_to_word = {v: k for k, v in tokenizer.word_index.items()}
    word_to_index = tokenizer.word_index

    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    target_seq[0, 0, word_to_index['<bos>']] = 1.

    stop_condition = False
    decoded_sentence = []
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = index_to_word.get(sampled_token_index, '')

        if sampled_word == '<eos>' or len(decoded_sentence) > max_length:
            stop_condition = True
        else:
            decoded_sentence.append(sampled_word)
            target_seq = np.zeros((1, 1, num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.
            states_value = [h, c]

    return ' '.join(decoded_sentence)


def evaluate_model():
    # Load tokenizer
    with open(os.path.join(config.save_model_path, 'tokenizer' + str(config.num_decoder_tokens)), 'rb') as file:
        tokenizer = joblib.load(file)

    # Load test data
    features, captions = load_test_data(config.test_path, tokenizer, config.max_length)

    # Load encoder model
    encoder_model = load_model(os.path.join(config.save_model_path, 'encoder_model.h5'))

    # Rebuild decoder model
    decoder_model, decoder_lstm, decoder_dense = build_inference_decoder(config.latent_dim, config.num_decoder_tokens)
    decoder_model.load_weights(os.path.join(config.save_model_path, 'decoder_model_weights.h5'))

    # Evaluate
    total_bleu = 0
    count = 0
    smooth = SmoothingFunction().method1
    for video_id in captions:
        input_seq = features[video_id].reshape(1, config.time_steps_encoder, config.num_encoder_tokens)
        decoded_sentence = decode_sequence(
            encoder_model, decoder_model, input_seq, tokenizer, config.max_length, config.num_decoder_tokens)

        # Choose one reference (or multiple if you prefer corpus-level BLEU)
        reference = [cap.split() for cap in captions[video_id]]
        candidate = decoded_sentence.split()

        bleu = sentence_bleu(reference, candidate, smoothing_function=smooth)
        print(f"[{video_id}] BLEU: {bleu:.4f} | Pred: {decoded_sentence}")
        total_bleu += bleu
        count += 1

    print(f"\nAverage BLEU score over {count} videos: {total_bleu / count:.4f}")


if __name__ == "__main__":
    evaluate_model()
