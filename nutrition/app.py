from flask import Flask, render_template, url_for, request, redirect
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Directory to save plots
if not os.path.exists('static'):
    os.makedirs('static')

# Path to the pre-downloaded CSV files
CSV_FILE_PATH = os.path.join('static', 'food_data.csv')
Y_LIMITS_FILE_PATH = os.path.join('static', 'y_limits.csv')

# Load the pre-downloaded CSV files globally
df = pd.read_csv(CSV_FILE_PATH)
y_limits_df = pd.read_csv(Y_LIMITS_FILE_PATH)

# Create a dictionary to store the max values for y-limits
y_limits = dict(zip(y_limits_df['food'], y_limits_df['max']))

@app.route('/')
def index():
    titles = df[df.columns[0]]

    # Check if a title has been selected
    selected_title = request.args.get('title')
    if selected_title and selected_title.isdigit():
        row_id = int(selected_title)
        return redirect(url_for('plot', row_id=row_id))

    return render_template('index.html', titles=titles)


@app.route('/plot/<int:row_id>')
def plot(row_id):
    # Get the specific row and its title
    row = df.iloc[row_id]
    title = row[df.columns[0]]
    
    # List to hold the paths to the generated plot images
    plot_filename = f'{title}_plots.png'
    plot_path = os.path.join('static', plot_filename)

    # Determine the number of features to plot
    features = df.columns[1:]  # Exclude the first column (food)

    # Filter features based on values greater than 0
    valid_features = [column for column in features if row[column] > 0]
    num_valid_features = len(valid_features)

    # Define the number of columns for layout
    num_cols = 6  # Set how many plots you want in one row
    num_rows = (num_valid_features + num_cols - 1) // num_cols  # Calculate required rows

    # Create a single figure with subplots arranged in a grid
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(3 * num_cols, 2 * num_rows))

    # Flatten the axes array for easy indexing
    axs = axs.flatten()

    # Loop through each valid feature for the given row
    for i, column in enumerate(valid_features):
        # Plot the column's data as a bar chart
        bar = axs[i].bar(column, row[column])
        # axs[i].set_xlabel('Feature')
        axs[i].set_ylabel('Daily Intake')
        # axs[i].set_title(f'{column} for {title}')
        
        if column in y_limits:
            axs[i].set_ylim(0, y_limits[column])

        for bar in axs[i].patches:
            axs[i].annotate(f'{bar.get_height():.1f}', 
                            (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                            ha='center', va='bottom')

    for j in range(i + 1, num_rows * num_cols):
        axs[j].axis('off')

    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    plot_url = url_for('static', filename=plot_filename) if num_valid_features > 0 else None

    return render_template('plot.html', title=title, plot_urls=[plot_url] if plot_url else [])

if __name__ == '__main__':
    app.run(debug=True)
