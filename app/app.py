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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Classify the image and get the predicted class name
        prediction = classify_image(filepath)
        return render_template('result.html', prediction=prediction, image_path=filepath)

    return "Error processing the image.", 500

if __name__ == '__main__':
    app.run(debug=True)
