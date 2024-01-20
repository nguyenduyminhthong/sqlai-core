from pydantic import BaseModel


class RelatedQuestion(BaseModel):
    sql: str
    question: str


class RelatedDDL(BaseModel):
    ddl: str


class RelatedDoc(BaseModel):
    doc: str
