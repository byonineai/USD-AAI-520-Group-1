from abc import ABC, abstractmethod
# @author: Marcelo Salvador
# This abstract class is a common interface with the DataProvider

class USDAnalysisStrategy(ABC):

    @abstractmethod
    def analyze(self, data):
        pass