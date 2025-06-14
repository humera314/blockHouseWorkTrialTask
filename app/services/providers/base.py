from abc import ABC, abstractmethod

class BaseMarketProvider(ABC):
    @abstractmethod
    def fetch_price(self, symbol: str) -> dict:
        pass