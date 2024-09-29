from flask import Flask, request, render_template
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    text = file.read().decode('utf-8')
    
    # Analyze text
    word_freq = pd.Series(text.split()).value_counts()
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400).generate(text)

    # Save word cloud image
    wordcloud_path = os.path.join('static', 'wordcloud.png')
    wordcloud.to_file(wordcloud_path)

    word_freq = pd.Series(...)  # Example, replace with your actual logic

    return render_template('index.html', word_freq=word_freq.to_dict(), wordcloud_path=wordcloud_path)

if __name__ == '__main__':
    app.run(debug=True)
