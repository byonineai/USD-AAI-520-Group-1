def main():
  print("The Autonomous Investment Research Agent Project")

from domain.research_task import ResearchTask, ResearchTaskType
from orchestration.research_planner import ResearchPlanner
def main():
    # task = ResearchTask(
    #     task_type=ResearchTaskType.MARKET,
    #     symbol="NVDA",
    # )

    # print(task)

    planner = ResearchPlanner()

    tasks = planner.plan("nvda")

    for task in tasks:
        print(
            f"{task.task_type.value}: {task.symbol}"
        )



if __name__ == "__main__":
  main()