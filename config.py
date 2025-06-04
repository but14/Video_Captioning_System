train_path = "data/training_data"
test_path = "data/testing_data"
batch_size = 320
learning_rate = 0.0007
epochs = 150
latent_dim = 512
num_encoder_tokens = 4096
num_decoder_tokens = 1500
time_steps_encoder = 80
max_probability = -1
save_model_path = 'model_final'
validation_split = 0.15
max_length = 10
# top_p, greedy
search_type = 'greedy' 
model_path = 'models/caption_model.h5'
tokenizer_path = "models/tokenizer.p"
max_caption_length = 34
cnn_output_dim = 2048
search_type_image = 'greedy'  # hoặc 'beam'

