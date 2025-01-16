import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load your model
MODEL_PATH = 'models/bacteria_classifier.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Load class labels (adjust based on your dataset)
CLASS_LABELS = ['Bacillus_Subtilis','Clostridium_Perfringens','Corynebacterium_Glutamicum','E_Coli','Mycobacterium_Tuberculosis_Smear', 'Neisseria_Gonorrheae_Smear', 
                'Paramecium_Plain_W.M', 'Pseudomonas_Aerogenosa', 'Salmonella_Typhosa', 
                'Streptococcus', 'Vibrio_Comma']  # Update these with your actual class names

# Define a confidence threshold (e.g., 0.6 = 60%)
CONFIDENCE_THRESHOLD = 0.6

def classify_image(image_path):
    # Load the image and preprocess it
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Rescale the image

    # Get model prediction
    predictions = model.predict(img_array)

    # Get the highest predicted class and its probability
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_probability = np.max(predictions)

    # If the model's confidence is below the threshold, classify it as "Unrecognized"
    if predicted_class_probability < CONFIDENCE_THRESHOLD:
        return "Unrecognized"

    # Return the class name
    return CLASS_LABELS[predicted_class_index]
