from abc import ABC, abstractmethod

class NewsDataProvider(ABC):

    @abstractmethod
    def get_financial_news(self, stock_symbol: str) -> dict:
#     """ Retrieve recent financial news when the user enters a stock symbol"""
        raise NotImplementedError
