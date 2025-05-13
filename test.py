from tensorflow.keras.models import load_model

try:
    model = load_model('D:\KHOALUAN\Video-Caption\model_final\encoder_model.h5')
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Failed to load model:", e)
