import re

import cohere

from base import ChatAgent
from schema import RelatedDDL, RelatedDoc, RelatedQuestion


class CohereAgent(ChatAgent):
    def __init__(self: "CohereAgent", api_key: str) -> None:
        self.llm_client = cohere.Client(api_key)

        return None

    def generate_sql(self: "CohereAgent", question: str, related_questions: list[RelatedQuestion], ddls: list[RelatedDDL], docs: list[RelatedDoc]) -> str:
        system_prompt = self._generate_sql_system_prompt(ddls, docs)
        prompt_history = self._generate_sql_prompt_history(related_questions)
        sql_response = self._submit_prompt(question, system_prompt, prompt_history)
        sql_response = self._postprocess_sql_response(sql_response)

        return sql_response

    def _submit_prompt(self: "CohereAgent", question: str, system_prompt: str, prompt_history: list[dict[str, str]] | None = None) -> str:
        response = self.llm_client.chat(question, chat_history=prompt_history, preamble_override=system_prompt).text

        return response

    def _generate_sql_system_prompt(self: "CohereAgent", ddls: list[RelatedDDL], docs: list[RelatedDoc]) -> str:
        system_prompt = "I provide a question, and you provide only SQL code without explaination.\n"

        system_prompt += "You may use the following DDL statements as a reference for what tables might be available:\n"
        for example in ddls:
            system_prompt += f"{example.ddl}\n"

        system_prompt += "You may use the following documentation as a reference for what tables might be available:\n"
        for example in docs:
            system_prompt += f"{example.doc}\n"

        return system_prompt

    def _generate_sql_prompt_history(self: "CohereAgent", related_questions: list[RelatedQuestion]) -> list[dict[str, str]]:
        prompt_history = []
        for example in related_questions:
            prompt_history.append({"role": "User", "message": example.question})
            prompt_history.append({"role": "Chatbot", "message": example.sql})

        return prompt_history

    def _postprocess_sql_response(self: "CohereAgent", sql_response: str) -> str:
        sql_response = re.findall(r"```sql(.*?)```", sql_response, re.DOTALL)[0]

        return sql_response
