from abc import ABC, abstractmethod

import pandas as pd


class ConnectorAgent(ABC):
    def __init__(self: "ConnectorAgent") -> None:
        self.connection = None

        return None

    @abstractmethod
    def connect(self: "ConnectorAgent", url: str) -> None:
        pass

    @abstractmethod
    def close(self: "ConnectorAgent") -> None:
        pass

    @abstractmethod
    def run(self: "ConnectorAgent", sql: str) -> pd.DataFrame | None:
        pass
