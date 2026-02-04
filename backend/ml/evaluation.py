from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

from .dataset import build_dataset
from .model import train_model


def evaluate_model(test_size=0.3, random_state=42):
    # Build dataset
    X, y = build_dataset()

    if len(X) < 5:
        raise ValueError(
            "Not enough data to evaluate ML model. "
            "Upload more documents first."
        )

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,    
        random_state=random_state,
        stratify=y
    )

    # Train model
    model = train_model(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 3),
        "roc_auc": round(roc_auc_score(y_test, y_prob), 3),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(
            y_test,
            y_pred,
            output_dict=True
        )
    }
