import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "credit_model.pkl")


def train_model(X, y):
    """
    Train ML creditworthiness model with proper scaling.
    This is interview-grade ML setup.
    """

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            max_iter=1000,
            solver="lbfgs"
        ))
    ])

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

    return model


def load_model():
    """
    Load trained ML model safely.
    """
    if not os.path.exists(MODEL_PATH):
        return None

    return joblib.load(MODEL_PATH)
