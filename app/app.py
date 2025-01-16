from flask import Flask, request, render_template, send_from_directory
import os
from classify import classify_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to classify uploaded image
@app.route('/classify', methods=['POST'])
def upload_and_classify():
    if 'file' not in request.files:
        return "No file uploaded!", 400

    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Classify the image and get the predicted title, description, safety, and probability
        title, description, safety, probability = classify_image(filepath)

        # Render the result page with these details
        return render_template('result.html', 
                               title=title, 
                               description=description, 
                               safety=safety, 
                               probability=probability, 
                               filename = file.filename)

    return "Error processing the image.", 500

if __name__ == '__main__':
    app.run(debug=True)
