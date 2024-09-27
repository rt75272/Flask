from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('house_price_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/house')
def house():
    return render_template('house.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        size = float(request.form['size'])
        prediction = model.predict(np.array([[size]]))
        rounded_prediction = round(prediction[0], 2)
        rounded_prediction = '{0:.2f}'.format(rounded_prediction)
        rounded_prediction = float(rounded_prediction)
        rounded_prediction = ('{:,}'.format(rounded_prediction))
        return render_template('house.html', prediction=rounded_prediction)
    except ValueError:
        return render_template('house.html', prediction="Invalid input! Please enter a numeric value.")
    except Exception as e:
        return render_template('house.html', prediction=f"An error occurred: {str(e)}")

@app.route('/data-analysis')
def data_analysis():
    return render_template('data_demo.html')


if __name__ == '__main__':
    app.run(debug=True)









