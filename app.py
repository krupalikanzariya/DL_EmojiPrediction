from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the trained tokenizer (update file name)
with open("tokenizer_0.3565.pkl", "rb") as file:
    tokenizer = pickle.load(file)

# Load the trained model (update file name)
model = tf.keras.models.load_model("emoji_prediction_model_0.3565.keras")

# Load emoji mappings from CSV
df = pd.read_csv("Mapping.csv")
category_to_emoji = dict(zip(df["number"], df["emoticons"]))

# Set max sequence length (matching the training data)
MAXLEN = 30  

# Initialize Flask app
app = Flask(__name__)

# Homepage Route
@app.route("/")
def home():
    return render_template("index.html", emojis=category_to_emoji)

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input
        user_input = request.form["text"]
        print(f"User input: {user_input}")

        # Tokenize and preprocess
        sequence = tokenizer.texts_to_sequences([user_input])
        padded_sequence = pad_sequences(sequence, maxlen=MAXLEN)
        
        # Model prediction
        prediction = model.predict(padded_sequence)
        predicted_class = np.argmax(prediction)
        print(f"Predicted class: {predicted_class}")

        # Get the corresponding emoji
        emoji_result = category_to_emoji.get(predicted_class, "❓")  # Default to ❓ if not found
        return jsonify({"prediction": emoji_result})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
