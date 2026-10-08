import json

from pathlib import Path
from dataclasses import asdict
from memory.usd_memory_repository import USDMemoryRespository
from domain.usd_research_memory import USDResearchMemory

class USDJsonMemoryRepository(USDMemoryRespository):

  def __init__(
    self,
    file_path: str = "memory/usd_research_memory.json"
  ):
    self.file_path = Path(file_path)

  def save(
    self,
    memory: USDResearchMemory # USD Research Memory is a dataclass
  ) -> None:

    all_stored_memories = self._load_all_values()
    # recursively convert dataclass instance winto a python dictionary
    all_stored_memories[memory.stock_symbol.upper()] = asdict(
      memory
    )

    self.file_path.parent.mkdir(
      parents = True,
      exist_ok=True
    )

    # it can be dumped with json
    with self.file_path.open(
      "w",
      encoding = "utf-8"
    ) as file:
        json.dump(
          all_stored_memories,
          file,
          indent=3
        )

  def get(
      self,
      stock_symbol: str
    ) -> USDResearchMemory | None:
      all_stored_memories = self._load_all_values()
      memory_data = all_stored_memories.get(
        stock_symbol.upper()
      )

      if memory_data is None:
        return None

      return USDResearchMemory(
        **memory_data
      )

  def _load_all_values(self) -> dict:

      if not self.file_path.exists():
        return {}

      with self.file_path.open(
        "r",
        encoding="utf-8"
      ) as file:

          return json.load(file)
