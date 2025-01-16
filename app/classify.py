import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template

# Load your model
MODEL_PATH = 'models/bacteria_classifier.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Load class titles, descriptions, and safety information
CLASS_TITLES = ['Bacillus Subtilis', 'Clostridium Perfringens', 'Corynebacterium Glutamicum', 'E. Coli', 
                'Mycobacterium Tuberculosis Smear', 'Neisseria Gonorrheae Smear', 'Paramecium Plain W.M', 
                'Pseudomonas Aerogenosa', 'Salmonella Typhosa', 'Streptococcus', 'Vibrio Comma']

CLASS_DESCRIPTIONS = [
    'A type of bacteria commonly found in soil and the intestines.',
    'A bacterium that causes food poisoning and gas gangrene.',
    'A bacterium used in the production of amino acids.',
    'A common bacterium associated with foodborne illness.',
    'A deadly bacterium causing tuberculosis.',
    'Bacterium that causes gonorrhea infection.',
    'A single-celled organism often found in water.',
    'A bacteria known for causing infections in humans.',
    'A bacterium responsible for causing typhoid fever.',
    'A genus of bacteria that can cause a range of diseases.',
    'A bacterium with a curved shape that can cause cholera.'
]

CLASS_SAFETY = [
    'Safe: Non-pathogenic bacterium found in soil and intestines.',
    'Harmful: Causes food poisoning and gas gangrene; can be life-threatening.',
    'Safe: Used in industrial amino acid production, not harmful.',
    'Harmful: Can cause foodborne illness, often linked to unclean food or water.',
    'Harmful: Highly contagious, causes tuberculosis, can be fatal.',
    'Harmful: Causes gonorrhea, a sexually transmitted infection.',
    'Safe: Protozoan organism, non-pathogenic, commonly found in aquatic environments.',
    'Harmful: Can cause infections in weakened immune systems, resistant to many antibiotics.',
    'Harmful: Can cause typhoid fever, which can be life-threatening without treatment.',
    'Harmful: Can cause various infections, including strep throat and pneumonia.',
    'Harmful: Can cause severe gastrointestinal illness, including cholera.'
]

# Define a confidence threshold (e.g., 0.6 = 60%)
CONFIDENCE_THRESHOLD = 0.6

# Flask app setup
app = Flask(__name__)

@app.route('/classify/<image_path>')
def classify(image_path):
    title, description, safety, probability = classify_image(image_path)
    # Render HTML with the data passed dynamically
    return render_template('result.html', 
                           title=title, 
                           description=description, 
                           safety=safety, 
                           probability=probability, 
                           image_path=image_path)

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
        return "Unrecognized", "The model could not confidently classify the image.", "N/A", "N/A"

    # Return the class title, description, safety, and probability
    class_title = CLASS_TITLES[predicted_class_index]
    class_description = CLASS_DESCRIPTIONS[predicted_class_index]
    class_safety = CLASS_SAFETY[predicted_class_index]
    return class_title, class_description, class_safety, predicted_class_probability

if __name__ == '__main__':
    app.run(debug=True)
