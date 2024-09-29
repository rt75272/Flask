from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Create a directory to save plots
if not os.path.exists('static/plots'):
    os.makedirs('static/plots')

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded!', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file!', 400

    # Read the uploaded file into a pandas DataFrame
    df = pd.read_csv(file)

    # Perform basic analysis
    summary = {
        'columns': df.columns.tolist(),
        'head': df.head().to_html(classes='data'),
        'describe': df.describe().to_html(classes='data')
    }

    # Generate a plot
    plot_filename = 'static/plots/plot.png'
    df.plot(kind='hist', alpha=0.5)
    plt.title('Histogram of Data')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.savefig(plot_filename)
    plt.close()

    return render_template('upload.html', summary=summary, plot=plot_filename)

if __name__ == '__main__':
    app.run(debug=True)
