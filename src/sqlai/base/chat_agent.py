from abc import ABC, abstractmethod

from sqlai.schema import RelatedDdl, RelatedDoc, RelatedQuestion


class ChatAgent(ABC):
    @abstractmethod
    def generate_sql(self: "ChatAgent", question: str, related_questions: list[RelatedQuestion], ddls: list[RelatedDdl], docs: list[RelatedDoc]) -> str:
        pass

    @abstractmethod
    def _submit_prompt(self: "ChatAgent", question: str, system_prompt: str, prompt_history: list[dict[str, str]] | None = None) -> str:
        pass

    @abstractmethod
    def _generate_sql_system_prompt(self: "ChatAgent", ddls: list[RelatedDdl], docs: list[RelatedDoc]) -> str:
        pass

    @abstractmethod
    def _generate_sql_prompt_history(self: "ChatAgent", related_questions: list[RelatedQuestion]) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def _postprocess_sql_response(self: "ChatAgent", sql_response: str) -> str:
        pass
