import yfinance as yf

from providers.market_data_provider import MarketDataProvider

class YahooFinanceProvider(MarketDataProvider):

    def get_market_data(self, symbol: str) -> dict:
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("The stock symbol can't be empty.")

        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            "symbol": symbol,
            "company_name": info.get("longName"),
            "current_price": info.get("currentPrice"),
            "pe_ratio": info.get("trailingPE"),
            "volume": info.get("volume"),
            "previous_close": info.get("previousClose"),
            "market_cap": info.get("marketCap"),
        }