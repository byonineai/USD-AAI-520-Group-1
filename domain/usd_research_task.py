from dataclasses import dataclass
# @Author: Marcelo Salvador
# Represents one piece of research the system must perform
# Data contracts between specialist agents and adapters.
@dataclass
class USDResearchTask:
    stock_symbol: str
    task_type: str