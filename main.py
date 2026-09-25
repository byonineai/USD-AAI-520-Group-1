def main():
  print("The Autonomous Investment Research Agent Project")

from domain.research_task import ResearchTask, ResearchTaskType

def main():
    task = ResearchTask(
        task_type=ResearchTaskType.MARKET,
        symbol="NVDA",
    )

    print(task)

if __name__ == "__main__":
  main()