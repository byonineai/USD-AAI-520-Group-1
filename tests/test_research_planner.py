from orchestration.research_planner import ResearchPlanner
from domain.research_task import ResearchTaskType
import pytest

def test_planner_creates_four_research_tasks():
  planner = ResearchPlanner()

  tasks = planner.plan("NVDA")

  assert len(tasks) == 4

  assert tasks[0].task_type == ResearchTaskType.MARKET
  assert tasks[1].task_type == ResearchTaskType.NEWS
  assert tasks[2].task_type == ResearchTaskType.EARNINGS
  assert tasks[3].task_type == ResearchTaskType.MACRO

def test_planner_normalizes_symbol():
  planner = ResearchPlanner()

  tasks = planner.plan(" nvda ")

  for task in tasks:
    assert task.symbol == "NVDA"

def test_planner_rejects_the_empty_symbol():
  planner = ResearchPlanner()

  with pytest.raises(ValueError):
    planner.plan("")
