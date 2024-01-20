from loguru import logger

from ..base import ConnectorAgent


class DummyConnectorAgent(ConnectorAgent):
    def connect(self: "DummyConnectorAgent", url: str) -> None:
        logger.warning(f"Connected to {url}")

        return None

    def close(self: "DummyConnectorAgent") -> None:
        logger.warning("Connection closed.")

        return None

    def run(self: "DummyConnectorAgent", _: str) -> None:
        logger.warning("If you want to run the SQL query, you should connect to a database first.")

        return None
