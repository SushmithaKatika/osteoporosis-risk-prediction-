# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

def train_model():
    # Sample dataset (use real-world data in production)
    data = {
        'age': [65, 70, 55, 80, 60],
        'gender': [1, 1, 0, 1, 0], # 1: Female, 0: Male
        'calcium_intake': [500, 700, 300, 400, 800],
        'bone_density': [0.5, 0.3, 0.7, 0.4, 0.6], # Example values
        'risk': [1, 1, 0, 0, 1]  # 1: High risk, 0: Low risk
    }

    df = pd.DataFrame(data)

    # Features and target
    X = df[['age', 'gender', 'calcium_intake', 'bone_density']]
    y = df['risk']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Test accuracy
    predictions = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions)}")

    # Save model
    with open('osteoporosis_model.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    train_model()
