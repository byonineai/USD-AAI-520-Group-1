from enum import Enum
# This is a vocabulary for the agent's state machine which helps prevent mistakes
class USDResearchState(Enum):
    PLANNING = "planning"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    AGGREGATING = "aggregating"
    GENERATING = "generating"

    # These will use these in later stages
    EVALUATING = "evaluating"
    OPTIMIZING = "optimizing"

    COMPLETE = "complete"

STATE_MESSAGES = {
    USDResearchState.PLANNING:
        "Please wait. Research planning in progress",

    USDResearchState.COLLECTING:
        "Please wait. Data collection in progress",

    USDResearchState.ANALYZING:
        "Please wait. Specialist analysis in progress",

    USDResearchState.AGGREGATING:
        "Please wait. Aggregating specialist results",

    USDResearchState.GENERATING:
        "Please wait. Report generation in progress",

    USDResearchState.EVALUATING:
        "Please wait. Evaluating research quality",

    USDResearchState.OPTIMIZING:
        "Please wait. Optimizing research results",

    USDResearchState.COMPLETE:
        "Research complete."
}