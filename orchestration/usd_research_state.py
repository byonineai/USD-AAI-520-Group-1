from enum import Enum

class USDResearchState(Enum):
    PLANNING = "planning"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    AGGREGATING = "aggregating"

    # These will use these in later stages
    EVALUATING = "evaluating"
    OPTIMIZING = "optimizing"

    COMPLETE = "complete"