import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("dataset/forestfires.csv")

# Select required columns
data = data[['temp', 'RH', 'wind', 'rain', 'area']]

# Create balanced fire risk classes
data['fire_risk'] = pd.qcut(
    data['area'],
    q=3,
    labels=['Low', 'Medium', 'High']
)



# Features
X = data[['temp', 'RH', 'wind', 'rain']]

# Target
y = data['fire_risk']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "forest_fire_model.pkl")

print("Model saved successfully!")