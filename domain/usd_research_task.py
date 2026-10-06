from dataclasses import dataclass
# @Author: Marcelo Salvador
# Represents one piece of research the system must perform

@dataclass
class USDResearchTask:
    stock_symbol: str
    task_type: str