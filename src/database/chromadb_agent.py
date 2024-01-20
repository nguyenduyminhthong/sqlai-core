import json

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from uuid import uuid4

from ..base import DatabaseAgent
from ..schema import RelatedDDL, RelatedDoc, RelatedQuestion


class ChromaDBAgent(DatabaseAgent):
    def __init__(self: "ChromaDBAgent", host: str) -> None:
        if not host:
            raise ValueError("Database host is not provided.")

        self.chroma_client = chromadb.HttpClient(host)
        self.sql_table = self.chroma_client.get_or_create_collection("sql", embedding_function=embedding_functions.DefaultEmbeddingFunction())
        self.ddl_table = self.chroma_client.get_or_create_collection("ddl", embedding_function=embedding_functions.DefaultEmbeddingFunction())
        self.doc_table = self.chroma_client.get_or_create_collection("doc", embedding_function=embedding_functions.DefaultEmbeddingFunction())

        return None

    def get_related_questions(self: "ChromaDBAgent", question: str) -> list[RelatedQuestion]:
        result = self.sql_table.query(query_texts=[question])
        if result["documents"]:
            return [RelatedQuestion.parse_raw(document) for document in result["documents"][0]]

        return []

    def get_related_ddls(self: "ChromaDBAgent", question: str) -> list[RelatedDDL]:
        result = self.ddl_table.query(query_texts=[question])
        if result["documents"]:
            return [RelatedDDL.parse_raw(document) for document in result["documents"][0]]

        return []

    def get_related_docs(self: "ChromaDBAgent", question: str) -> list[RelatedDoc]:
        result = self.doc_table.query(query_texts=[question])
        if result["documents"]:
            return [RelatedDoc.parse_raw(document) for document in result["documents"][0]]

        return []

    def get_training_data(self: "ChromaDBAgent") -> pd.DataFrame:
        df = pd.DataFrame()

        sql_data = self.sql_table.get()
        if sql_data is not None:
            documents = [json.loads(document) for document in sql_data["documents"]]

            df_sql = pd.DataFrame({"id": sql_data["ids"], "content": map(lambda document: document["sql"], documents), "question": map(lambda document: document["quest"], documents)})

            df = pd.concat([df, df_sql])

        ddl_data = self.ddl_table.get()
        if ddl_data is not None:
            documents = [json.loads(document) for document in ddl_data["documents"]]

            df_ddl = pd.DataFrame({"id": ddl_data["ids"], "content": map(lambda document: document["ddl"], documents)})
            df_ddl["question"] = None

            df = pd.concat([df, df_ddl])

        doc_data = self.doc_table.get()
        if doc_data is not None:
            documents = [json.loads(document) for document in doc_data["documents"]]

            df_doc = pd.DataFrame({"id": doc_data["ids"], "content": map(lambda document: document["ddl"], documents)})
            df_doc["question"] = None

            df = pd.concat([df, df_doc])

        return df

    def add_sql_question(self: "ChromaDBAgent", sql: str, question: str) -> None:
        uuid = str(uuid4()) + "-sql"
        self.sql_table.add(uuid, documents=json.dumps({"sql": sql, "question": question}))

        return None

    def add_ddl(self: "ChromaDBAgent", ddl: str) -> None:
        uuid = str(uuid4()) + "-ddl"
        self.ddl_table.add(uuid, documents=json.dumps({"ddl": ddl}))

        return None

    def add_doc(self: "ChromaDBAgent", doc: str) -> None:
        uuid = str(uuid4()) + "-doc"
        self.doc_table.add(uuid, documents=json.dumps({"doc": doc}))

        return None

    def remove_training_data(self: "ChromaDBAgent", uuid: str) -> bool:
        if uuid.endswith("-sql"):
            self.sql_table.delete([uuid])
            return True
        elif uuid.endswith("-ddl"):
            self.ddl_table.delete([uuid])
            return True
        elif uuid.endswith("-doc"):
            self.doc_table.delete([uuid])
            return True
        else:
            return False
