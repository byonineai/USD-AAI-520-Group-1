from agents.usd_analysis_strategy import USDAnalysisStrategy
from orchestration.usd_agent_registry import USDAgentRegistry
# @Author: Marcelo Salvador

# Given a task type, select the appropriate specialist
# Which agent should receive this task

class USDAgentRouter:

    def __init__(self, registry: USDAgentRegistry):
        self.registry = registry

    def route(self, task_type: str) -> USDAnalysisStrategy:
        return self.registry.get(task_type)