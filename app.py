from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import config
from predict_realtime import VideoDescriptionRealTime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

video_input = VideoDescriptionRealTime(config)

@app.route('/api/predict', methods=['POST'])
def predict_caption():
    """
    Nhận request Json hoặc file video, trả về caption của video đó
    """
    file_name = None

    # Nếu là upload file
    if 'file' in request.files:
        video_file = request.files['file']
        if video_file.filename == '':
            return jsonify({'error': 'No file uploaded'}), 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(file_path)
        file_name = file_path
    else:
        # Nếu là gửi URL (YouTube)
        data = request.get_json()
        if not data or 'file_name' not in data:
            return jsonify({'error': 'No filename provided'}), 400
        file_name = data['file_name']

    try:
        # Chú ý: get_test_data cần truyền file_name vào nếu bạn muốn lấy đặc trưng từ file vừa upload
        X_test, _ = video_input.get_test_data(file_name)
        if config.search_type == 'greedy':
            caption = video_input.greedy_search(X_test.reshape((-1, 80, 4096)))
            video_caption = caption
        else:
            decoded_sentence = video_input.decode_sequence2bs(X_test.reshape((-1, 80, 4096)))
            decoded_str = video_input.decoded_sentence_tuning(decoded_sentence)
            video_caption = ''.join(decoded_str)

        video_input.max_prob = -1
        return jsonify({'caption': video_caption.strip()}), 200
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({'error': 'An error occurred during prediction: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)