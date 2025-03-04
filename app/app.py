import os
from flask import Flask, request, render_template
from app.classify import classify_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def upload_and_classify():
    if 'file' not in request.files:
        return "No file uploaded!", 400

    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Classify the image and get the predicted title, description, safety, and probability
        title, description, safety, probability = classify_image(filepath)

        # Render the result page with these details
        return render_template('result.html', 
                              title=title, 
                              description=description, 
                              safety=safety, 
                              probability=probability, 
                              filename=filename)

    return "Error processing the image.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)