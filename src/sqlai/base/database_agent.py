from abc import ABC, abstractmethod

import pandas as pd

from ..schema import RelatedDdl, RelatedDoc, RelatedQuestion


class DatabaseAgent(ABC):
    @abstractmethod
    def get_related_questions(self: "DatabaseAgent", question: str) -> list[RelatedQuestion]:
        pass

    @abstractmethod
    def get_related_ddls(self: "DatabaseAgent", question: str) -> list[RelatedDdl]:
        pass

    @abstractmethod
    def get_related_docs(self: "DatabaseAgent", question: str) -> list[RelatedDoc]:
        pass

    @abstractmethod
    def get_training_data(self: "DatabaseAgent") -> pd.DataFrame:
        pass

    @abstractmethod
    def add_sql_question(self: "DatabaseAgent", sql: str, question: str) -> None:
        pass

    @abstractmethod
    def add_ddl(self: "DatabaseAgent", ddl: str) -> None:
        pass

    @abstractmethod
    def add_doc(self: "DatabaseAgent", doc: str) -> None:
        pass

    @abstractmethod
    def remove_training_data(self: "DatabaseAgent", uuid: str) -> bool:
        pass
