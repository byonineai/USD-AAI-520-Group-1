from dataclasses import dataclass
# Data contracts between specialist agents and adapters.
@dataclass
class USDOptimizationAction:
  '''
  Optimization action determines what should happen next.
  '''
  action: str
  reason: str
  task_type: str | None = None
