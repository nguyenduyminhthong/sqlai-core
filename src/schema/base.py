from pydantic import BaseModel


class RelatedQuestion(BaseModel):
    sql: str
    question: str


class RelatedDdl(BaseModel):
    ddl: str


class RelatedDoc(BaseModel):
    doc: str
