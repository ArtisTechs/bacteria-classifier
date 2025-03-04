import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template

# Load your model
MODEL_PATH = 'models/bacteria_classifier.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Load class titles, descriptions, and safety information
CLASS_TITLES = ['Bacillus Subtilis', 'Clostridium Perfringens', 'Corynebacterium Glutamicum', 'Escherichia coli', 
                'Mycobacterium Tuberculosis Smear', 'Neisseria Gonorrheae Smear', 'Paramecium Plain W.M', 
                'Pseudomonas Aerogenosa', 'Salmonella Typhosa', 'Streptococcus', 'Vibrio Comma']

CLASS_DESCRIPTIONS = [
    'Known as hay bacillus or grass bacillus, is a gram-positive, catalase-positive bacterium, found in soil and gastrointestinal tract of ruminants, humans and marine sponges.',
    'A Gram-positive, anaerobic, rod-shaped bacterium from the Clostridium genus. It is both heat-resistant and cold-tolerant, surviving in conditions with little or no oxygen. C. perfringens makes people sick by making spores, which have protective coatings. After a person eats food contaminated with the C. perfringens, the bacteria can make a toxin (poison) that causes diarrhea.',
    'Is a Gram-positive, rod-shaped bacterium that is used industrially for large-scale production of amino acids, especially glutamic acid and lysine.',
    'Escherichia coli are Gram-negative, short rod-shaped bacteria and members of the family Enterobacteriaceae. Infections due to E. coli (Escherichia coli) bacteria can cause severe, bloody diarrhea. Sometimes they also cause urinary tract infections, pneumonia, meningitis, bacteremia (a bacterial infection in the blood), or sepsis (a dangerous full-body response to bacteremia).',
    'Mycobacterium tuberculosis, also known as Koch’s bacillus, is a species of pathogenic bacteria in the family Mycobacteriaceae and causative agent of tuberculosis. First discovered in 1882 by Robert Koch. Tuberculosis is a chronic, progressive mycobacterial infection, often with an asymptomatic latent period following initial infection. Tuberculosis most commonly affects the lungs.',
    'Also known as gonococcus or gonococci, is a species of gram-negative diplococci bacteria. Gonorrhoea is a common sexually transmitted infection caused by a type of bacteria. It usually spreads through vaginal, oral or anal sex. Gonorrhoea is treatable and curable with antibiotics.',
    'It is not gram-positive or gram-negative. It is a genus of unicellular ciliated protozoa. They are characterised by the presence of thousands of cilia covering their body. They are found in freshwater, marine and brackish water. They are also found attached to the surface. Reproduction is primarily through asexual means (binary fission)',
    'Is a Gram-negative bacterium that can cause infections in people with weakened immune systems. It is commonly found in soil, water, and on skin. Known for its resistance to many antibiotics, it can cause pneumonia, urinary tract infections, skin infections, and more.',
    'A genus of rod-shaped, gram-negative bacteria of the family Enterobacteriaceae. Typhoid fever is an illness you get from S. Typhi bacterium. It causes a high fever, flu-like symptoms and diarrhea. You can be contagious with typhoid even if you don’t feel sick. Typhoid can be life-threatening and should be treated promptly with antibiotics. If you live in or travel to an area where typhoid is common, you should get vaccinated.',
    'A genus of gram-positive or spherical bacteria that belongs to the family Streptococcaceae. Streptococcus (GAS) is a type of bacteria that can cause skin, soft tissue and respiratory tract infections. It is spread from person-to-person through respiratory droplets such as from coughing or sneezing and from touching skin or other surfaces contaminated with bacteria.',
    'Genus Vibrio is Gram-negative, with a curved-rod (comma) shape and several species cause fish diseases. They are typically found in salt water, and they are facultative anaerobe and oxidase positive. Vibrio infections can cause a range of symptoms, including diarrhea, stomach cramps, nausea, vomiting, fever, and chills.'
]

CLASS_SAFETY = [
    'Safe',
    'Harmful',
    'Safe',
    'Neutral',
    'Harmful',
    'Harmful',
    'Safe',
    'Harmful',
    'Harmful',
    'Harmful',
    'Harmful'
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
