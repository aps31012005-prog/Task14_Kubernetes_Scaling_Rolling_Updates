from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)


# ==========================================
# CIFAR-10 Class Names
# ==========================================

class_names = [
    "Airplane",
    "Automobile",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck"
]


# ==========================================
# Load Trained CNN Model
# ==========================================

MODEL_PATH = "model/cifar10_cnn.keras"

model = tf.keras.models.load_model(MODEL_PATH)


# ==========================================
# Home / Health Check Endpoint
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "CIFAR-10 Flask Prediction API is running",
        "endpoint": "/predict",
        "method": "POST"
    })


# ==========================================
# Prediction Endpoint
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    # Check whether image was provided
    if "image" not in request.files:
        return jsonify({
            "error": "No image provided. Please upload an image."
        }), 400

    try:

        # Get uploaded image
        image_file = request.files["image"]

        # Open image and convert to RGB
        image = Image.open(image_file).convert("RGB")

        # Resize image to CIFAR-10 input size
        image = image.resize((32, 32))

        # Convert image to NumPy array
        image_array = np.array(image)

        # Normalize pixel values
        image_array = image_array.astype("float32") / 255.0

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        # Make prediction
        predictions = model.predict(
            image_array,
            verbose=0
        )

        # Find predicted class
        predicted_index = np.argmax(predictions[0])

        predicted_class = class_names[predicted_index]

        # Calculate confidence
        confidence = float(predictions[0][predicted_index]) * 100

        # Return JSON response
        return jsonify({
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )