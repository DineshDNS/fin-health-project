import pandas as pd
from analysis.models import DocumentAnalysis
from .features import extract_features


def build_dataset():
    rows = []
    labels = []

    for analysis in DocumentAnalysis.objects.all():
        features = extract_features(analysis)
        rows.append(features)

        # Label: 1 = GOOD, 0 = RISKY
        labels.append(1 if analysis.risk_level == "LOW" else 0)

    X = pd.DataFrame(rows)
    y = pd.Series(labels)

    return X, y
