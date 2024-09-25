import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

from flask import Flask, render_template, url_for
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
    # Extract the first column as titles (used for links)
    titles = df[df.columns[0]]
    
    # Render the index.html template and pass the list of titles
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
    num_cols = 4  # Set how many plots you want in one row
    num_rows = (num_valid_features + num_cols - 1) // num_cols  # Calculate required rows

    # Create a single figure with subplots arranged in a grid
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4.5 * num_cols, 2 * num_rows))  # Adjusted size here

    # Flatten the axes array for easy indexing
    axs = axs.flatten()

    # Loop through each valid feature for the given row
    for i, column in enumerate(valid_features):
        # Plot the column's data as a bar chart (for a single value, row[column])
        bar = axs[i].bar(column, row[column])

        # Set the x and y axis labels and title
        axs[i].set_xlabel('Feature')  # X-axis: column name
        axs[i].set_ylabel('Value')  # Y-axis: the value of the row in this column
        axs[i].set_title(f'{column} for {title}')  # Title from the first column and the current column name
        
        # Set y-limits based on y_limits dictionary
        if column in y_limits:
            axs[i].set_ylim(0, y_limits[column])  # Set y-limits

        # Add the numeric value on top of the bar
        for bar in axs[i].patches:  # Iterate through each bar
            axs[i].annotate(f'{bar.get_height():.1f}',  # Format the height value
                            (bar.get_x() + bar.get_width() / 2, bar.get_height()),  # Position above the bar
                            ha='center', va='bottom')  # Centered horizontally, bottom vertically

    # Hide any unused subplots
    for j in range(i + 1, num_rows * num_cols):
        axs[j].axis('off')  # Hide the unused axes

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Save the combined plot
    plt.savefig(plot_path)
    plt.close()

    # Only add plot URL if there are valid features to plot
    if num_valid_features > 0:
        plot_url = url_for('static', filename=plot_filename)
    else:
        plot_url = None  # No valid features, no plot to show

    # Render the plot.html template and pass the title and the plot URL
    return render_template('plot.html', title=title, plot_urls=[plot_url] if plot_url else [])


if __name__ == '__main__':
    app.run(debug=True)
