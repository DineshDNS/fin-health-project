from .models import CumulativeAnalysisState


def get_cumulative_state():
    state, _ = CumulativeAnalysisState.objects.get_or_create(id=1)
    return state
