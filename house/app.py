from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('house_price_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the size from the form
    size = float(request.form['size'])
    
    # Make a prediction
    prediction = model.predict(np.array([[size]]))
    
    # Round the prediction to 2 decimal places
    rounded_prediction = round(prediction[0], 2)
    rounded_prediction = '{0:.2f}'.format(rounded_prediction)
    rounded_prediction = float(rounded_prediction)
    rounded_prediction = ('{:,}'.format(rounded_prediction))
    
    return render_template('index.html', prediction=rounded_prediction)

if __name__ == '__main__':
    app.run(debug=True)
