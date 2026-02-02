from features.bank_features import compute_bank_features
from features.gst_features import compute_gst_features


def build_feature_store(parsed_data: dict, doc_type: str) -> dict:
    """
    Central feature store
    """

    if doc_type == "BANK":
        return {
            "bank_features": compute_bank_features(parsed_data)
        }

    if doc_type == "GST":
        return {
            "gst_features": compute_gst_features(parsed_data)
        }

    return {}
