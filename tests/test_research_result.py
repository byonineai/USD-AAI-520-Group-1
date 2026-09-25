from domain.research_result import ResearchResult
from domain.research_task import ResearchTaskType


def test_research_result_stores_normalized_data():
    result = ResearchResult(
        task_type=ResearchTaskType.MARKET,
        symbol="NVDA",
        data={
            "price": 100.00,
        },
    )

    assert result.task_type == ResearchTaskType.MARKET
    assert result.symbol == "NVDA"
    assert result.data["price"] == 100.00