def merge_gst(state, data):
    state.taxable_value += data["taxable_value"]
    state.gst_paid += data["gst_paid"]
    state.expected_gst += data["expected_gst"]

    state.payment_ratio = (
        state.gst_paid / state.expected_gst
        if state.expected_gst else 1
    )

    state.compliance_gap = state.expected_gst - state.gst_paid
    state.is_compliant = state.payment_ratio >= 0.95
