from abc import ABC, abstractmethod
from trading_bot.logger import logger

class Strategy(ABC):
    def __init__(self, name, portfolio):
        self.name = name
        self.portfolio = portfolio
        logger.info(f"Initialized strategy: {self.name}")

    @abstractmethod
    def on_data(self, data):
        """
        Called when new data is available.
        strategies should implement their logic here.
        """
        pass

    def log(self, message):
        logger.info(f"[{self.name}] {message}")
