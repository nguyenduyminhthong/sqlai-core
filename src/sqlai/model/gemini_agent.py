import re

import google.generativeai as genai

from sqlai.base import ChatAgent
from sqlai.schema import RelatedDdl, RelatedDoc, RelatedQuestion


class GeminiAgent(ChatAgent):
    def __init__(self: "GeminiAgent", api_key: str) -> None:
        genai.configure(api_key=api_key)

        self.llm_client = genai.GenerativeModel("gemini-1.0-pro-001")

        return None

    def generate_sql(self: "GeminiAgent", question: str, related_questions: list[RelatedQuestion], ddls: list[RelatedDdl], docs: list[RelatedDoc]) -> str:
        system_prompt = self._generate_sql_system_prompt(ddls, docs)
        prompt_history = self._generate_sql_prompt_history(related_questions)
        sql_response = self._submit_prompt(question, system_prompt, prompt_history)
        sql_response = self._postprocess_sql_response(sql_response)

        return sql_response

    def _submit_prompt(self: "GeminiAgent", question: str, system_prompt: str, prompt_history: list[dict[str, str]] | None = None) -> str:
        prompt_history.insert(0, {"role": "user", "parts": [system_prompt]})
        prompt_history.insert(1, {"role": "model", "parts": ["Understood."]})
        prompt_history.append({"role": "user", "parts": [question]})

        response = self.llm_client.generate_content(prompt_history).candidates[0].content.parts[0].text

        return response

    def _generate_sql_system_prompt(self: "GeminiAgent", ddls: list[RelatedDdl], docs: list[RelatedDoc]) -> str:
        system_prompt = "I provide a question, and you provide only SQL code without explanation.\n"

        system_prompt += "You may use the following DDL statements as a reference for what tables might be available:\n"
        for example in ddls:
            system_prompt += f"{example.ddl}\n"

        system_prompt += "You may use the following documentation as a reference for what tables might be available:\n"
        for example in docs:
            system_prompt += f"{example.doc}\n"

        return system_prompt

    def _generate_sql_prompt_history(self: "GeminiAgent", related_questions: list[RelatedQuestion]) -> list[dict[str, str]]:
        prompt_history = []
        for example in related_questions:
            prompt_history.append({"role": "user", "parts": [example.question]})
            prompt_history.append({"role": "model", "parts": [example.sql]})

        return prompt_history

    def _postprocess_sql_response(self: "GeminiAgent", sql_response: str) -> str:
        try:
            sql_response = re.findall(r"```sql(.*?)```", sql_response, re.DOTALL)[0]
        except IndexError:
            pass

        return sql_response
