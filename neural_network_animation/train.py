import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Create a sample dataset
data = {
    'size': [1500, 1600, 1700, 1800, 1900, 2000],
    'price': [300000, 320000, 340000, 360000, 380000, 400000]
}
df = pd.DataFrame(data)

# Split the data
X = df[['size']]
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'house_price_model.pkl')
