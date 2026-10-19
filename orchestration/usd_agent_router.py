from agents.usd_analysis_strategy import USDAnalysisStrategy
from orchestration.usd_agent_registry import USDAgentRegistry
# @Author: Marcelo Salvador

class USDAgentRouter:
    '''
    The role of this class is to select the correct specialist agent for a specific task type.
    This class answers which agent should handle this task?
    '''
    def __init__(self, registry: USDAgentRegistry):
        self.registry = registry

    def route(self, task_type: str) -> USDAnalysisStrategy:
        return self.registry.get(task_type)