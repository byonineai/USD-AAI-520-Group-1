from dataclasses import dataclass

@dataclass
class USDOptimizationAction:
  '''
  Optimization action determines what should happen next.
  '''
  action: str
  reason: str
  task_type: str | None = None
