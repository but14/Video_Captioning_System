import os
import numpy as np
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
import pickle

class ImageCaptioning:
    def __init__(self, model_path, tokenizer_path, max_caption_length=34, cnn_output_dim=2048, search_type='greedy'):
        # Load model và tokenizer
        self.caption_model = load_model(model_path)
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)
        self.max_caption_length = max_caption_length
        self.cnn_output_dim = cnn_output_dim
        self.search_type = search_type

        # Chuẩn bị model trích xuất đặc trưng ảnh
        base_model = InceptionV3(weights='imagenet')
        self.feature_model = Model(base_model.input, base_model.layers[-2].output)

    def extract_image_features(self, image_path):
        img = load_img(image_path, target_size=(299, 299))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = self.feature_model.predict(img)
        return features

    def greedy_search(self, image_features):
        in_text = 'start'
        for _ in range(self.max_caption_length):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=self.max_caption_length, padding='post')
            yhat = self.caption_model.predict([image_features, sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = self.tokenizer.index_word.get(yhat, '')
            in_text += ' ' + word
            if word == 'end' or word == '':
                break
        in_text = in_text.replace('start ', '').replace(' end', '')
        return in_text

    def beam_search(self, image_features, K_beams=3):
        start = [self.tokenizer.word_index['start']]
        start_word = [[start, 0.0]]
        for _ in range(self.max_caption_length):
            temp = []
            for s in start_word:
                sequence = pad_sequences([s[0]], maxlen=self.max_caption_length, padding='post')
                preds = self.caption_model.predict([image_features, sequence], verbose=0)
                word_preds = np.argsort(preds[0])[-K_beams:]
                for w in word_preds:
                    next_cap, prob = s[0][:], s[1]
                    next_cap.append(w)
                    prob += np.log(preds[0][w] + 1e-10)
                    temp.append([next_cap, prob])
            start_word = sorted(temp, key=lambda l: l[1])[-K_beams:]
        best_sequence = start_word[-1][0]
        captions_ = [self.tokenizer.index_word.get(i, '') for i in best_sequence]
        final_caption = []
        for word in captions_:
            if word == 'end':
                break
            if word != 'start' and word != '':
                final_caption.append(word)
        return ' '.join(final_caption)

    def predict(self, image_path, mode='greedy'):
        features = self.extract_image_features(image_path)
        if mode == 'greedy':
            return self.greedy_search(features)
        else:
            return self.beam_search(features, K_beams=3)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True, help="Path to image file")
    parser.add_argument('--mode', default='greedy', choices=['greedy', 'beam'], help="Decoding mode")
    parser.add_argument('--model', default='models/caption_model.keras', help="Path to model file")
    parser.add_argument('--tokenizer', default='models/tokenizer.p', help="Path to tokenizer file")
    parser.add_argument('--maxlen', type=int, default=34, help="Max caption length")
    args = parser.parse_args()

    captioner = ImageCaptioning(
        model_path=args.model,
        tokenizer_path=args.tokenizer,
        max_caption_length=args.maxlen,
        cnn_output_dim=2048,
        search_type=args.mode
    )

    print(f"Extracting features from: {args.image}")
    caption = captioner.predict(args.image, mode=args.mode)
    print("\nPredicted Caption:")
    print(caption)
    