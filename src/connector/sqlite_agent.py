import os
import sqlite3
from urllib.parse import urlparse

import pandas as pd
import requests
from loguru import logger

from ..base import ConnectorAgent


class SQLiteAgent(ConnectorAgent):
    def connect(self: "SQLiteAgent", url: str) -> None:
        path = os.path.basename(urlparse(url).path)

        if not os.path.exists(url):
            try:
                response = requests.get(url)
            except Exception as e:
                logger.critical(f"Invalid URL: {url}")
                raise e

            with open(path, "wb") as f:
                f.write(response.content)

            url = path

        self.connection = sqlite3.connect(url)
        logger.success(f"Connected to {url}")

        return None

    def close(self: "SQLiteAgent") -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.success("Connection closed.")

        return None

    def run(self: "SQLiteAgent", sql: str) -> pd.DataFrame | None:
        if not self.connection:
            logger.warning("If you want to run the SQL query, you should connect to a database first.")
            return None

        try:
            df = pd.read_sql_query(sql, self.connection)
            logger.info(df)
            return df

        except Exception as e:
            logger.error(f"Could not run sql command: {e}")
            raise e
